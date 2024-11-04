from flask import Blueprint, jsonify

doctor_routes = Blueprint('doctor', __name__)

@doctor_routes.route('/test')
def testget():
    return jsonify({"this": "works"})