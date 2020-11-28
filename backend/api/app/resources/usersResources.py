from flask import request, Blueprint, make_response, jsonify
from flask_restful import Api, Resource

from ..common.Schemas.UserSchema import UserSchema, UserSearchSchema, UserByEmailSchema
from ..common.Schemas.NotificationSchema import NotificationSchema
from ..common.Schemas.CurriculumSchema import CurriculumSchema
from ..database.UserModel import User
from ..database.CurriculumModel import Curriculum
from ..database.EducationModel import Education
from ..database.LanguageModel import Language
from ..database.WorkExperienceModel import WorkExperience
from ..database.NotificationModel import Notification
from ..database.CategoryModel import Category
from ..database.Curriculum_CategoryModel import Curriculum_Category
from ..database.StatsQuery import median, medianFreelance

from ..common.error_handling import ObjectNotFound, Forbidden, BadRequest

from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

from marshmallow.exceptions import ValidationError

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


class UserCurriculumR(Resource):
    def get(self, id):
        user_id = validateToken(request, ['cliente', 'funcionario'])
        u = User.get_by_id(user_id)
        if u.id == id or u.role == 'funcionario':
            u = User.get_by_id(id)
            if u is not None:
                if u.curriculum != []:
                    res = {
                    'msg': 'Ok',
                    'results': CurriculumSchema().dump(u.curriculum[0])
                    }
                    return make_response(jsonify(res), 200)
                raise ObjectNotFound('No existe ningun curriculum asociado al usuario indicado.')
            raise ObjectNotFound("No existe el usuario indicado.")
        raise Forbidden('No tienes permisos para realizar esta acción.')

    def post(self, id):
        user_id = validateToken(request, 'cliente')
        if user_id == id:
            u = User.get_by_id(user_id)
            if u.curriculum == []:
                try:
                    data = CurriculumSchema().load(request.get_json())
                    c = Curriculum(data['name'])
                    c.birth_date = data['birth_date']
                    c.phone = data['phone']
                    c.country = data['country']
                    c.address = data['address']
                    if 'avatar' in data and data['avatar'] is not None:
                        c.avatar = data['avatar']
                    if 'description' in data and data['description'] is not None:
                        c.description = data['description']
                    if 'education' in data and data['education'] is not None:
                        for edu in data['education']:
                            e = Education(edu['name'])
                            e.place = edu['place']
                            e.start_date = edu['start_date']
                            if 'end_date' in edu and edu['end_date'] is not None:
                                e.end_date = edu['end_date']
                            c.education.append(e)
                    if 'workexperience' in data and data['workexperience'] is not None:
                        for wexp in data['workexperience']:
                            we = WorkExperience(wexp['name'])
                            we.ocupation = wexp['ocupation']
                            we.start_date = wexp['start_date']
                            if 'end_date' in wexp and wexp['end_date'] is not None:
                                we.end_date = wexp['end_date']
                            c.workexperience.append(we)
                    if 'languages' in data and data['languages'] is not None:
                        for lan in data['languages']:
                            l = Language(lan['name'])
                            c.languages.append(l)
                    ccList =  []
                    if 'categories' in data and data['categories'] is not None:
                        for cat in data['categories']:
                            category = Category.get_by_id(cat['category']['id'])
                            cc = Curriculum_Category()
                            cc.category_id = cat['category']['id']
                            cc.curriculum_id = 0
                            ccList.append(cc)
                    u.curriculum.append(c)
                    u.save()
                    for cc in ccList:
                        cc.curriculum_id = u.curriculum[0].id
                        cc.save()
                    res = {
                        'msg': 'Ok',
                        'results': CurriculumSchema().dump(c)
                    }
                    return make_response(jsonify(res), 201)
                except ValidationError as err:
                    raise BadRequest(err.messages)
            raise BadRequest('Ya tienes un curriculum ingresado.')
        raise Forbidden('No tienes permisos para realizar esta accion.')

    def put(self, id):
        user_id = validateToken(request, 'cliente')
        if user_id == id:
            u = User.get_by_id(user_id)
            if u.curriculum != []:
                try:
                    data = CurriculumSchema().load(request.get_json())
                    c = Curriculum(data['name'])
                    c.birth_date = data['birth_date']
                    c.phone = data['phone']
                    c.country = data['country']
                    c.address = data['address']
                    if 'avatar' in data and data['avatar'] is not None:
                        c.avatar = data['avatar']
                    if 'description' in data and data['description'] is not None:
                        c.description = data['description']
                    if 'education' in data and data['education'] is not None:
                        for edu in data['education']:
                            e = Education(edu['name'])
                            e.place = edu['place']
                            e.start_date = edu['start_date']
                            if 'end_date' in edu and edu['end_date'] is not None:
                                e.end_date = edu['end_date']
                            c.education.append(e)
                    if 'workexperience' in data and data['workexperience'] is not None:
                        for wexp in data['workexperience']:
                            we = WorkExperience(wexp['name'])
                            we.ocupation = wexp['ocupation']
                            we.start_date = wexp['start_date']
                            if 'end_date' in wexp and wexp['end_date'] is not None:
                                we.end_date = wexp['end_date']
                            c.workexperience.append(we)
                    if 'languages' in data and data['languages'] is not None:
                        for lan in data['languages']:
                            l = Language(lan['name'])
                            c.languages.append(l)
                    ccList =  []
                    if 'categories' in data and data['categories'] is not None:
                        for cat in data['categories']:
                            category = Category.get_by_id(cat['category']['id'])
                            cc = Curriculum_Category()
                            cc.category_id = cat['category']['id']
                            cc.curriculum_id = 0
                            ccList.append(cc)
                    u.curriculum[0].user_id = None
                    u.curriculum.append(c)
                    u.save()
                    for cc in ccList:
                        cc.curriculum_id = u.curriculum[0].id
                        cc.save()
                    res = {
                        'msg': 'Ok',
                        'results': CurriculumSchema().dump(c)
                    }
                    return make_response(jsonify(res), 200)
                except ValidationError as err:
                    raise BadRequest(err.messages)
            raise ObjectNotFound('No existe ningun curriculum asociado al usuario indicado.')
        raise Forbidden('No tienes permisos para realizar esta accion.')


class UserSalaryR(Resource):
    def get(self, id):
        user_id = validateToken(request, 'cliente')
        if user_id == id:
            u = User.get_by_id(id)
            if u.curriculum[0] is not None:
                resList = []
                for c in u.curriculum[0].categories:
                    obj = {'name': c.category.name, 'estimation': 0, 'median': 0, 'minimum': 0, 'maximum': 0, 'freelance': {'estimation': 0, 'median': 0, 'minimum': 0, 'maximum': 0}}
                    cat = Category.get_by_id(c.category.id)
                    jobs = cat.subcategories[0].jobs
                    total = 0
                    count = 0
                    minimum = 0
                    maximum = 0
                    totalF = 0
                    countF = 0
                    minimumF = 0
                    maximumF = 0
                    for j in jobs:
                        if 'workana' in j.url:
                            if j.salary is not None and j.salary < 100000 and j.active == True:
                                if minimumF == 0 or j.salary < minimumF:
                                    minimumF = j.salary
                                if j.salary > maximumF:
                                    maximumF = j.salary
                                totalF = totalF + j.salary
                                countF = countF + 1
                        else:
                            if j.salary is not None and j.salary < 100000 and j.active == True:
                                if minimum == 0 or j.salary < minimum:
                                    minimum = j.salary
                                if j.salary > maximum:
                                    maximum = j.salary
                                total = total + j.salary
                                count = count + 1    
                    if count > 0:
                        obj['estimation'] = int(total / count)
                    else:
                        obj['estimation'] = 'Desconocido'
                    if countF > 0:
                        obj['freelance']['estimation'] = int(totalF / countF)
                    else:
                        obj['freelance']['estimation'] = 'Desconocido'
                    obj['minimum'] = minimum
                    obj['maximum'] = maximum
                    obj['freelance']['minimum'] = minimumF
                    obj['freelance']['maximum'] = maximumF
                    # m = median(c.category.id)[0]['mediana']
                    # mF = medianFreelance(c.category.id)
                    # if m is not None:
                    #     obj['median'] = m
                    # if 'mediana' in mF and mF is not None:
                    #     obj['freelance']['median'] = mF['mediana']
                    resList.append(obj)
                res = {
                    'msg': 'Ok',
                    'results': resList
                }
                return make_response(jsonify(res), 200)
            raise ObjectNotFound('No existe un curriculum asociado a este usuario.')
        raise Forbidden('No tienes permisos para realizar esta accion.')


api.add_resource(UserGetNotificationsR, '/api/users/<int:id>/notifications')
api.add_resource(UserNotificationUpdateR,
                 '/api/users/<int:id>/notifications/<int:nId>')
api.add_resource(UserCurriculumR,
                 '/api/users/<int:id>/curriculum')
api.add_resource(UserSalaryR,
                 '/api/users/<int:id>/salary')


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

class UsersRecommendedRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        users = None
        if 'jobId' in data and data['jobId'] is not None:
            users = Curriculum.get_all_by_job_id(data['jobId'])
        elif 'filters' in data and data['filters'] is not None:
            users = Curriculum.get_all_recommended_users_by_filters(data)
        else:
            raise BadRequest('No se indicaron campos necesarios para realizar la operación.')
        res = {
            'results': UserByEmailSchema().dump(users, many=True)
        }
        return make_response(jsonify(res), 200)


api.add_resource(UserByIdRA, '/api/users/a/<int:id>')
api.add_resource(UserByEmailRA, '/api/users/a/email')
api.add_resource(UsersSearchByEmailRA, '/api/users/a/searchbyemail')
api.add_resource(UsersRecommendedRA, '/api/users/a/recommended')
