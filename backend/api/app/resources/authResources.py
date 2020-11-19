from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.UserSchema import UserSchema
from ..database.UserModel import User

from ..common.error_handling import ObjectNotFound

from ..common.token_helper import generate_token

from datetime import datetime

auth_bp = Blueprint('auth_bp', __name__)

user_schema = UserSchema()

api = Api(auth_bp)


class SignUpResource(Resource):
    def post(self):
        data = request.get_json()
        user_dict = user_schema.load(data)
        u = User.get_by_email(user_dict['email'])
        if u is not None:
            res = {
                'msg': 'Email already exists.'
            }
            return make_response(jsonify(res), 202)
        user = User(email=user_dict['email'],
                    password=user_dict['password'])
        user.save()
        result = user_schema.dump(user)
        return result, 201

class SignInResource(Resource):
    def post(self):
        data = request.get_json()
        print(type(data))
        user_dict = user_schema.load(data)
        user = User.get_by_email(user_dict['email'])
        if user is not None and user.password_is_valid(user_dict['password']):
            access_token = generate_token(user.id, user.role)
            if access_token:
                user.last_login = datetime.utcnow()
                user.save()
                res = {
                    'msg': 'You logged in successfully',
                    'userSession': {
                        'access_token': access_token.decode(),
                        'id': user.id,
                        'email': user.email,
                        'role': user.role
                    }
                }    
                return make_response(jsonify(res), 200)
        else:
            res = {
                    'msg': 'Credenciales invalidas'
                }    
            return make_response(jsonify(res), 401)

class EmailResource(Resource):
    def post(self):
        email = False
        data = request.get_json()
        user = User.get_by_email(data['email'])
        if user is not None:
            email = True
        res = {
            'email': email
        }
        return make_response(jsonify(res), 200)


api.add_resource(SignUpResource, '/api/auth/signup/',
                 endpoint='signup_resource')
api.add_resource(SignInResource, '/api/auth/signin/',
                 endpoint='signin_resource')
api.add_resource(EmailResource, '/api/auth/email/',
                 endpoint='email_resource')
