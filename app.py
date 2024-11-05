
from flask import Flask

from routes.doctorroutes import doctor_routes

from routes.userroutes import user_routes


'''

To run app - flask run --debug

To configure tailwind CSS 
1.npm install -D tailwindcss
2.npx tailwindcss init
3.npx tailwindcss -i ./static/styles/style.css -o ./static/styles/output.css --watch

'''

app = Flask(__name__)

app.register_blueprint(doctor_routes, url_prefix='/doc')
app.register_blueprint(user_routes)

app.secret_key = "veryprivatekey"
