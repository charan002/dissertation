from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import session
from flask import redirect

from pymongo import MongoClient

from validator import signup_validator
from validator import login_validator

'''

To run app - flask run --debug

'''

cient = MongoClient()

client = MongoClient('mongodb://localhost:27017/')
db = client.projectdb
collection = db.mycollection

app = Flask(__name__)
app.secret_key = 'veryprivatekey'

def isUserAuthenticated():
    if session.get('username') != None and collection.find_one({'username': session.get('username')}) != None:
        return True
    return False

def identifyTypeOfUser():
    return session.get('usertype')

@app.before_request
def isAuthenticated():
    try:
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

@app.route('/')
def home():
    data = {
        'username': session.get('username')
    }
    return render_template('home.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/signup', methods=['GET', 'POST'])
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
        
@app.route('/logout')
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
    
@app.route('/testmongo')
def mongo_test():
    documents_list = list(collection.find())
    for doc in documents_list:
        doc['_id'] = None
    return jsonify(documents_list)
    
