from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, jsonify, session, redirect

from validator import signup_validator, login_validator

from mongoclient import db

user_routes = Blueprint('user', __name__)

collection = db["user"]
doc_collection = db["doctor"]
time_reporting_collection = db["timereporting"]
appointments_collection = db["appointments"]

@user_routes.route('/test')
def testget():
    return jsonify({"this": "works"})

def isUserAuthenticated():
    if session.get('username') != None and collection.find_one({'username': session.get('username')}) != None:
        return True
    return False

def identifyTypeOfUser():
    return session.get('usertype')

def changeObjectId(data):
    for item in data:
        item['_id'] = str(item['_id'])

@user_routes.before_request
def isAuthenticated():
    try:
        if (request.path in ['/testmongo', '/doc/test']):
            return
        if (request.path == '/login' or request.path == '/signup') and request.method == 'GET':
            if isUserAuthenticated():
                user_type = identifyTypeOfUser()
                if user_type == 'user':
                    return redirect('/')
        else:
            if (request.path != '/login' and request.path != '/signup') and not isUserAuthenticated():
                return redirect('/login')
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})

@user_routes.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        try:
            return render_template('login.html')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})
    elif request.method == 'POST':
        try:
            data = {
                'username': request.form.get('username'),
                'password': request.form.get('password')
            }
            login_validator(data)
            user_db_data = collection.find_one({'username': data.get('username')})
            if user_db_data != None and data.get('password') == user_db_data['password']:
                session['username'] = data.get('username')
                session['usertype'] = 'user'
                print('authenticated')
                return redirect('/')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})

@user_routes.route('/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        try:
            data = {
                'username': request.form.get('username'),
                'firstname': request.form.get('firstname'),
                'lastname': request.form.get('lastname'),
                'phonenumber': request.form.get('phonenumber'),
                'password': request.form.get('password')
            }
            signup_validator(data)
            collection.insert_one(data)
            session['username'] = request.form.get('username')
            session['usertype'] = 'user'
            return redirect('/')
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        
@user_routes.route('/logout')
def user_logout():
    try:
        if(session.get('username')!= None):
            session.pop('username')
            session.pop('usertype')
            return redirect('/login')
        else:
            return redirect('/login')
    except:
        return jsonify({'error':'logout error'}),500
    
@user_routes.route('/')
def home():
    today = datetime.today().strftime('%Y-%m-%d')
    appointments = list(appointments_collection.find({'$and': [
            {'username': session.get('username')},
            {'date': {'$ne': today}}
        ]}))
    changeObjectId(appointments)
    todayAppointments = list(appointments_collection.find({'$and': [
        {'date': today},
        {'username': session.get('username')}
    ]}))
    print(todayAppointments)
    changeObjectId(todayAppointments)
    for item in appointments:
        date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
        item['date'] = date_obj.strftime("%Y-%b-%d")
    for item in todayAppointments:
        date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
        item['date'] = date_obj.strftime("%Y-%b-%d")
    data = {
        'username': session.get('username'),
        'appointments': appointments,
        'todayAppointments': todayAppointments
    }
    return render_template('home.html', data=data)
    
@user_routes.post('/getsearchresults')
def get_search_results():
    try:
        print(request.get_json())
        data = list(doc_collection.find({'doctortype': request.get_json()['doctype']}))
        print(data)
        timeRepData = list(time_reporting_collection.find({'$and': [
            {'date': {'$eq': request.get_json()['date']}}
        ]}))
        final_list = []
        changeObjectId(data)
        changeObjectId(timeRepData)
        for i in timeRepData:
            for j in data:
                if i['doctorid'] == j['doctorid']:
                    j = {
                        **j, **i
                    }
                    final_list.append(j)
        return jsonify(final_list)
    except Exception as e:
        return jsonify({'error': f'generic error {str(e)}'})

@user_routes.post('/submit/appointment')
def submit_appointment():
    try:
        data = {
            **request.get_json(),
            'username': session.get('username')
        }
        appointments_collection.insert_one(data)
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})

@user_routes.route('/testmongo')
def mongo_test():
    documents_list = list(collection.find())
    for doc in documents_list:
        doc['_id'] = None
    return jsonify(documents_list)
    

@user_routes.route('/remarksandprescriptions')
def get_remarks_and_prescriptions():
    try:
        user_data = list(appointments_collection.find({'$and': [
            {'username': session.get('username')},
            {'status': 'DONE'}
        ]}))
        changeObjectId(user_data)
        for item in user_data:
            date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
            item['displayDate'] = date_obj.strftime("%Y-%b-%d")
        data = {
            'remarksAndPrescriptions': user_data
        }
        return render_template('remarksandprescriptions.html', data=data)
    except Exception as e:
        return jsonify({'error': f'{e}'})