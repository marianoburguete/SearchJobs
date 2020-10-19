from flask import request, Blueprint, make_response, jsonify
from flask_restful import Api, Resource

from ..common.Schemas.UserSchema import UserSchema, UserSearchSchema, UserByEmailSchema
from ..common.Schemas.NotificationSchema import NotificationSchema
from ..database.UserModel import User
from ..database.CurriculumModel import Curriculum
from ..database.NotificationModel import Notification

from ..common.error_handling import ObjectNotFound, Forbidden

from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse


users_bp = Blueprint('users_bp', __name__)

user_schema = UserSchema()

api = Api(users_bp)


class UserGetNotificationsR(Resource):
    def get(self, id):
        user_id = validateToken(request, 'cliente')
        count = Notification.unreadNotificationsCount(id)
        res = {
            'msg': 'Ok',
            'results': {
                'count': count
            }
        }
        return make_response(jsonify(res), 200)

    def post(self, id):
        user_id = validateToken(request, 'cliente')
        data = request.get_json()
        if user_id == id:
            return makePagResponse(Notification.get_pag(data, id), NotificationSchema())
        raise Forbidden('No tienes permisos para realizar esta accion.')


class UserNotificationUpdateR(Resource):
    def get(self, id, nId):
        user_id = validateToken(request, 'cliente')
        if user_id == id:
            n = Notification.get_by_id(nId)
            if n is not None:
                n.status = 'readed'
                n.save()
                return 'Ok', 200
            raise ObjectNotFound('No existe la notificacion indicada')
        raise Forbidden('No tienes permisos para realizar esta accion.')


api.add_resource(UserGetNotificationsR, '/api/users/<int:id>/notifications')
api.add_resource(UserNotificationUpdateR,
                 '/api/users/<int:id>/notifications/<int:nId>')


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
