from flask import Flask

from routes.doctorroutes import doctor_routes

from routes.userroutes import user_routes


'''

To run app - flask run --debug

'''

app = Flask(__name__)

app.register_blueprint(doctor_routes, url_prefix='/doc')
app.register_blueprint(user_routes)

app.secret_key = "veryprivatekey"
