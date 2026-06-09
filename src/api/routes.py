from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from flask_cors import CORS
from sqlalchemy import select, func
from api.models import db, User

api = Blueprint('api', __name__)

CORS(api)

@api.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    response = [user.serialize() for user in users]
    return jsonify(response), 200
    
@api.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User (firstname = data.get("firstname"))
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({"msg": "Usuario creado"}), 201
    
    