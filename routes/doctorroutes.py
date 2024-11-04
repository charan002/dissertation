from flask import Blueprint, jsonify, request, render_template, session, redirect

from mongoclient import db

from validator import doctor_login_validator, doctor_signup_validator

doctor_routes = Blueprint('doctor', __name__)

collection = db["doctor"]

def isDoctorAuthenticated():
    if session.get('doctorid') != None and collection.find_one({'doctorid': session.get('doctorid')}) != None:
        return True
    return False

def identifyTypeOfUser():
    return session.get('usertype')

@doctor_routes.before_request
def isAuthenticated():
    try:
        if (request.path in ['/doc/test']):
            return
        if (request.path == '/doc/login' or request.path == '/doc/register') and request.method == 'GET':
            if isDoctorAuthenticated():
                user_type = identifyTypeOfUser()
                if user_type == 'doctor':
                    return redirect('/doc/')
        else:
            if (request.path != '/doc/login' and request.path != '/doc/register') and not isDoctorAuthenticated():
                return redirect('/doc/login')
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})

@doctor_routes.route('/login', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'GET':
        try:
            return render_template('doctor/login.html')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})
    elif request.method == 'POST':
        try:
            data = {
                'doctorid': request.form.get('doctorid'),
                'password': request.form.get('password')
            }
            doctor_login_validator(data)
            user_db_data = collection.find_one({'username': data.get('username')})
            if user_db_data != None and data.get('password') == user_db_data['password']:
                session['doctorid'] = data.get('doctorid')
                session['usertype'] = 'doctor'
                print('authenticated')
                return redirect('/doc/')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})
        
@doctor_routes.route('/register', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template('doctor/register.html')
    elif request.method == 'POST':
        try:
            print('post req', request.form)
            data = {
                'doctorid': request.form.get('doctorid'),
                'firstname': request.form.get('firstname'),
                'lastname': request.form.get('lastname'),
                'phonenumber': request.form.get('phonenumber'),
                'doctortype': request.form.get('doctortype'),
                'password': request.form.get('password')
            }
            print(data)
            doctor_signup_validator(data)
            collection.insert_one(data)
            session['doctorid'] = request.form.get('doctorid')
            session['usertype'] = 'doctor'
            return redirect('/doc/')
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        
@doctor_routes.route('/logout')
def user_logout():
    try:
        if(session.get('doctorid')!= None):
            session.pop('doctorid')
            session.pop('usertype')
            return redirect('/doc/login')
        else:
            return redirect('/doc/login')
    except:
        return jsonify({'error':'logout error'}),500
    

@doctor_routes.route('/')
def home():
    data = {
        'doctorid': session.get('doctorid')
    }
    return render_template('doctor/home.html', data=data)

@doctor_routes.route('/test')
def testget():
    return jsonify({"this": "works"})
    