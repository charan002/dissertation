from flask import Blueprint, jsonify, request, render_template, jsonify, session, redirect

from validator import signup_validator, login_validator

from mongoclient import db

user_routes = Blueprint('user', __name__)

collection = db.mycollection

@user_routes.route('/test')
def testget():
    return jsonify({"this": "works"})


def isUserAuthenticated():
    if session.get('username') != None and collection.find_one({'username': session.get('username')}) != None:
        return True
    return False

def identifyTypeOfUser():
    return session.get('usertype')

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
                elif user_type == 'doctor':
                    return redirect('/doc/home')
        else:
            if (request.path != '/login' and request.path != '/signup') and not isUserAuthenticated():
                return redirect('/login')
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})

@user_routes.route('/')
def home():
    data = {
        'username': session.get('username')
    }
    return render_template('home.html', data=data)

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
    
@user_routes.route('/testmongo')
def mongo_test():
    documents_list = list(collection.find())
    for doc in documents_list:
        doc['_id'] = None
    return jsonify(documents_list)
    