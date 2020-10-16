from flask import request, Blueprint, make_response, jsonify
from flask_restful import Api, Resource

from ..common.Schemas.UserSchema import UserSchema, UserSearchSchema, UserByEmailSchema
from ..database.UserModel import User
from ..database.CurriculumModel import Curriculum

from ..common.error_handling import ObjectNotFound

from ..common.token_helper import validateToken


users_bp = Blueprint('users_bp', __name__)

user_schema = UserSchema()

api = Api(users_bp)


class UserListResource(Resource):
    def get(self):
        user_id = validateToken(request, 'funcionario')
        users = User.get_all()
        result = user_schema.dump(users, many=True)
        return result
    
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = User.get_by_email()


api.add_resource(UserListResource, '/api/users/',
                 endpoint='user_list_resource')

# ADMIN ENDPOINTS

class UserByIdRA(Resource):
    def get(self, id):
        user_id = validateToken(request, 'funcionario')
        u = User.get_by_id(id)
        res = {
            'user': UserSchema().dump(u)
        }
        return make_response(jsonify(res), 200)

class UserByEmailRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        u = User.get_by_email(request.get_json()['email'])
        res = {
            'user': UserByEmailSchema().dump(u)
        }
        return make_response(jsonify(res), 200)

class UsersSearchByEmailRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        u = User.search_by_email(request.get_json()['email'])
        res = {
            'users': UserByEmailSchema().dump(u, many=True)
        }
        return make_response(jsonify(res), 200)

api.add_resource(UserByIdRA, '/api/users/a/<int:id>')
api.add_resource(UserByEmailRA, '/api/users/a/email')
api.add_resource(UsersSearchByEmailRA, '/api/users/a/searchbyemail')