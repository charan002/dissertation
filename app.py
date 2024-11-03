from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import session
from flask import redirect

from pymongo import MongoClient

from validator import signup_validator
from validator import login_validator

cient = MongoClient()

client = MongoClient("mongodb://localhost:27017/")
db = client.projectdb
collection = db.mycollection

app = Flask(__name__)
app.secret_key = "veryprivatekey"

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        try:
            if session.get("username") != None and collection.find_one({"username": session.get("username")}) != None:
                print("redirecting")
                return redirect("/")
            print("rendering template")
            return render_template('login.html')
        except Exception as e:
            return jsonify({"error": f"generic error {str(e)}"})
    elif request.method == 'POST':
        try:
            data = {
                "username": request.form.get("username"),
                "password": request.form.get("password")
            }
            login_validator(data)
            user_db_data = collection.find_one({"username": data.get("username")})
            if user_db_data != None and data.get("password") == user_db_data["password"]:
                session["username"] = data.get("username")
                return redirect("/")
        except Exception as e:
            return jsonify({"error": f"generic error {str(e)}"})

@app.route("/signup", methods=['GET', 'POST'])
def user_signup():
    if request.method == 'GET':
        if session.get("username") != None and collection.find_one({"username": session.get("username")}) != None:
            return redirect("/")
        return render_template('signup.html')
    elif request.method == 'POST':
        try:
            data = {
                "firstname": request.form.get('firstname'),
                "lastname": request.form.get('lastname'),
                "phonenumber": request.form.get('phonenumber'),
                "password": request.form.get('password')
            }
            signup_validator(data)
            collection.insert_one(data)
            session["username"] = request.form.get('username')
            return redirect('/')
        except Exception as e:
            print(e)
            return jsonify({'error': str(e)}), 500
        
@app.route("/logout")
def user_logout():
    try:
        if(session.get("username")!= None):
            session.pop("username")
            return redirect("/login")
        else:
            return redirect("/login")
    except:
        return jsonify({'error':'logout error'}),500
    
@app.route("/testmongo")
def mongo_test():
    documents_list = list(collection.find())
    for doc in documents_list:
        doc["_id"] = None
    return jsonify(documents_list)
    
