from flask import Blueprint, make_response, jsonify, request

from app import LOG
from models.administration import User
from repository.setup_sqlalchemy import sql_engine
from repository.user import UserRepository
from utilities.authentication import create_token, auth

user_repo = UserRepository(sql_engine)
user_routes = Blueprint( 'user', __name__ )

@user_routes.route("/users/create", methods=['POST'])
def create_user():
    try:
        data = request.get_json(force=True)
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        if user_repo.get_by_username(username):
            return make_response('username taken', 400)
        user = user_repo.create(User(
            _id=-1,
            username=username,
            email=email,
            password=password
        ))
        return make_response('', 200)
    except Exception as e:
        return make_response('', 500)

@user_routes.route("/users/all", methods=['GET'])
def all_users():
    user_repo = UserRepository(sql_engine)
    lst = user_repo.all()
    return jsonify(lst)

@user_routes.route("/login", methods=['POST'])
def login():
    try:
        data = request.get_json(force=True)
        username = request.json['username']
        password = request.json['password']

        user = user_repo.get_by_username(username)
        if user is None or user.password != password:
            LOG.info('g')
            return make_response('invalid login', 401)

        token = create_token(username)
        return jsonify({'token': token})
    except Exception as e:
        return make_response('', 500)

@user_routes.route("/users/info", methods=['GET'])
@auth
def user_info(user: User):
    return jsonify({
        'username': user.username,
        'email': user.email
    })
