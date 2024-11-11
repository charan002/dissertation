from flask import Blueprint, jsonify, request, render_template, session, redirect

from mongoclient import db

from validator import doctor_login_validator, doctor_signup_validator

from datetime import datetime

from bson import ObjectId

doctor_routes = Blueprint('doctor', __name__)

collection = db["doctor"]
timeReportCollection = db["timereporting"]
appointmentsCollection = db['appointments']

def isDoctorAuthenticated():
    if session.get('doctorid') != None and collection.find_one({'doctorid': session.get('doctorid')}) != None:
        return True
    return False

def identifyTypeOfUser():
    return session.get('usertype')

def changeObjectId(data):
    for item in data:
        item['_id'] = str(item['_id'])

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
                return redirect('/doc/')
        except Exception as e:
            return jsonify({'error': f'generic error {str(e)}'})
        
        
@doctor_routes.route('/register', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        return render_template('doctor/register.html')
    elif request.method == 'POST':
        try:
            data = {
                'doctorid': request.form.get('doctorid'),
                'firstname': request.form.get('firstname'),
                'lastname': request.form.get('lastname'),
                'phonenumber': request.form.get('phonenumber'),
                'hospitalname': request.form.get('hospitalname'),
                'doctortype': request.form.get('doctortype'),
                'password': request.form.get('password')
            }
            doctor_signup_validator(data)
            collection.insert_one(data)
            session['doctorid'] = request.form.get('doctorid')
            session['usertype'] = 'doctor'
            return redirect('/doc/')
        except Exception as e:
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
    today = datetime.today().strftime('%Y-%m-%d')
    time_data = list(timeReportCollection.find({'doctorid': session.get('doctorid'), 'date': today}))
    time_data_future = list(timeReportCollection.find({'doctorid': session.get('doctorid'), 'date': {'$gt': today}}))
    doc_info = collection.find_one({'doctorid': session.get('doctorid')})
    appointment_info = list(appointmentsCollection.find({'doctorid': session.get('doctorid')}))
    for item in appointment_info:
        date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
        item['displayDate'] = date_obj.strftime("%Y-%b-%d")
    for doc in time_data:
        doc['_id'] = str(doc['_id'])
    changeObjectId(appointment_info)
    changeObjectId(time_data_future)
    data = {
        'doctorid': session.get('doctorid'),
        'timeReporting': time_data,
        'futureTimeReporting': time_data_future,
        'hospital': doc_info.get('hospitalname'),
        'appointments': appointment_info
    }
    return render_template('doctor/home.html', data=data)

@doctor_routes.post('/submit/timereport')
def submit_time_report():
    data = {
        'doctorid': session['doctorid'],
        **request.get_json()
    }
    timeReportCollection.insert_one(data)
    return jsonify({"tjos": "wor"})

@doctor_routes.post('/appointment/changestatus')
def change_appointment_status():
    try:
        appointmentsCollection.update_one({'_id': ObjectId(request.get_json()['id'])}, {'$set': {'status': request.get_json()['statusChange']}})
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})

@doctor_routes.get('/patientdetails')
def render_patient_details():
    username = request.args.get('username')
    id = request.args.get('id')
    appointment_data = list(appointmentsCollection.find({'_id': ObjectId(id)}))
    user_appointments = list(appointmentsCollection.find({'$and': [
        {'doctorid': session.get('doctorid')},
        {'username': username}
    ]}))
    all_user_appointments_db = list(appointmentsCollection.find({'$and': [
        {"$nor": [{"doctorid": session.get("doctorid")}]},
        {"username": username}
    ]}))
    for item in all_user_appointments_db:
        date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
        item['displayDate'] = date_obj.strftime("%Y-%b-%d")
    changeObjectId(all_user_appointments_db)
    print(all_user_appointments_db)
    all_user_appointments = {}
    for item in all_user_appointments_db:
        if all_user_appointments.get(item['hospitalname']) is None:
            all_user_appointments[item['hospitalname']] = [item]
        else:
            all_user_appointments[item['hospitalname']].append(item)
    data = {
        'currentAppointment': appointment_data,
        'allUserAppointments': user_appointments,
        'otherUserAppointments': all_user_appointments
    }
    for item in user_appointments:
        date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
        item['displayDate'] = date_obj.strftime("%Y-%b-%d")
    changeObjectId(data['currentAppointment'])
    changeObjectId(data['allUserAppointments'])
    return render_template('/doctor/patientdetails.html', data=data)

@doctor_routes.post('/submit/prescriptionAndRemarks')
def submit_prescription():
    try:
        id = request.get_json()['id']
        appointmentsCollection.update_one({'_id': ObjectId(id)}, {'$set': {
            'prescription': request.get_json()['prescription'],
            'remarks': request.get_json()['remarks']
            }})
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({'error': f'{str(e)}'})


@doctor_routes.post('/test')
def testget():
    return jsonify({"this": "works"})
    

