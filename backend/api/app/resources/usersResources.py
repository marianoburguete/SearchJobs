from flask import request, Blueprint, make_response, jsonify
from flask_restful import Api, Resource

from ..common.Schemas.UserSchema import UserSchema
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


api.add_resource(UserListResource, '/api/users/',
                 endpoint='user_list_resource')
