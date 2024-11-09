from flask import Blueprint, jsonify, request, render_template, session, redirect

from mongoclient import db

pharma_routes = Blueprint('pharma', __name__)

collection = db["pharma"]
user_collection = db["user"]
appointments_collection = db["appointments"]

#def prescriptions(data):
 #   if data.get('phonenumber')

def isPharmaAuthenticated():
    if session.get('pharmaid') != None and collection.find_one({'pharmaid': session.get('pharmaid')}) != None:
        return True
    return False

def identifyTypeOfUser():
    return session.get('usertype')

def changeObjectId(data):
    for item in data:
        item['_id'] = str(item['_id'])


@pharma_routes.before_request
def isAuthenticated():
    try:
        if (request.path in ['/pharma/test']):
            return
        if (request.path == '/pharma/login' or request.path == '/pharma/register') and request.method == 'GET':
            if isPharmaAuthenticated():
                user_type = identifyTypeOfUser()
                if user_type == 'pharmacist':
                    return redirect('/pharma/')
        else:
            if (request.path != '/pharma/login' and request.path != '/pharma/register') and not isPharmaAuthenticated():
                return redirect('/pharma/login')
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})
    
@pharma_routes.route('/login', methods=['GET', 'POST'])
def pharma_login():
    if request.method == 'GET':
        try:
            return render_template('pharma/login.html')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})
    elif request.method == 'POST':
        try:
            data = {
                'pharmaid': request.form.get('pharmaid'),
                'password': request.form.get('password')
            }
            user_db_data = collection.find_one({'username': data.get('username')})
            if user_db_data != None and data.get('password') == user_db_data['password']:
                session['pharmaid'] = data.get('pharmaid')
                session['usertype'] = 'pharmacist'
                print('authenticated')
                return redirect('/pharma/')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})
        
@pharma_routes.route('/register', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template('/pharma/register.html')
    elif request.method == 'POST':
        try:
            print('post req', request.form)
            data = {
                'pharmaid': request.form.get('pharmaid'),
                'firstname': request.form.get('firstname'),
                'lastname': request.form.get('lastname'),
                'phonenumber': request.form.get('phonenumber'),
                'pharmacyname': request.form.get('pharmacyname'),
                'password': request.form.get('password')
            }
            print(data)
            collection.insert_one(data)
            session['pharmaid'] = request.form.get('pharmaid')
            session['usertype'] = 'pharmacist'
            return redirect('/pharma/')
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500

@pharma_routes.route('/logout')
def user_logout():
    try:
        print(session.items())
        if(session.get('pharmaid')!= None):
            session.pop('pharmaid')
            session.pop('usertype')
            return redirect('/pharma/login')
        else:
            return redirect('/pharma/login')
    except:
        return jsonify({'error':'logout error'}),500
    
@pharma_routes.route('/')
def home():
    data = {
        'pharmaid': session.get('pharmaid'),
    }
    return render_template('pharma/home.html', data=data)

@pharma_routes.post('/getPrescriptions')
def get_prescriptions():
    data = request.get_json()
    #print(data)
    #print(data.get('phoneNumber'))
    doc = list(user_collection.find({'phonenumber': data.get('phoneNumber')}))
    #print(doc[0].get('phonenumber'))
    #print(doc[0].get('username'))
    aptmts = list(appointments_collection.find({'$and': [
            {'username': doc[0].get('username')},
            {'status': "DONE"}
        ]}))
    #print(aptmts)
    for items in aptmts:
        print(items.get('prescription', 'Prescription not found'))
    changeObjectId(aptmts)
    return jsonify(aptmts)

