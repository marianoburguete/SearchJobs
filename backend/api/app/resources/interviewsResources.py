from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from marshmallow import ValidationError

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema
from ..common.Schemas.InterviewSchema import InterviewSchema, InterviewGetUserSchema, InterviewPutSchema, InterviewGetAllSchema, InterviewGetAllResponseSchema
from ..common.Schemas.MessageSchema import MessageSchema
from ..database.JobModel import Job
from ..database.UserModel import User
from ..database.InterviewModel import Interview
from ..database.MessageModel import Message
from ..database.CompanyModel import Company
from ..database.RequirementModel import Requirement
from ..database.ApplicationModel import Application
from ..database.NotificationModel import Notification

from ..common.error_handling import ObjectNotFound, BadRequest, Forbidden
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json
from datetime import datetime

interviews_bp = Blueprint('interviews_bp', __name__)

interview_schema = InterviewSchema()
interview_get_user_schema = InterviewGetUserSchema()
interview_put_schema = InterviewPutSchema()

api = Api(interviews_bp)


class IdInterviewR(Resource):
    def get(self, id):
        user_id = validateToken(request, 'cliente')
        i = Interview.get_by_id(id)
        if i is not None:
            if i.to_user == user_id:
                res = {
                'msg': 'Ok.',
                'results': interview_get_user_schema.dump(i)
                }
                return make_response(jsonify(res), 200)
            raise Forbidden('No tienes permisos para acceder a esta entrevista.')
        raise ObjectNotFound('No existe la entrevista para el Id dado.')


class GetAllByUserR(Resource):
    def post(self, id):
        user_id = validateToken(request, 'cliente')
        if user_id == id:
            data = InterviewGetAllSchema().load(request.get_json())
            pagResult = Interview.get_pag(data)
            return makePagResponse(pagResult, InterviewGetAllResponseSchema())
        raise BadRequest('No tienes los permisos necesarios')


# class GetScheduleUser(Resource):
#     def get(self, id):
#         user_id = validateToken(request, 'cliente')
#         if user_id == id:
#             pagResult = Interview.get_pag(data)
#             return makePagResponse(pagResult, InterviewGetAllResponseSchema())
#         raise BadRequest('No tienes los permisos necesarios')


class MessagesR(Resource):
    def post(self, id):
        user_id = validateToken(request, ['funcionario', 'cliente'])
        i = Interview.get_by_id(id)
        if i is not None:
            u = User.get_by_id(user_id)
            if u.role == 'funcionario' or user_id == i.to_user:
                i.messages.append(Message(user_id, request.get_json()['text']))
                i.save()
                if u.role == 'funcionario':
                    n = Notification(i.to_user, 'Nuevo mensaje', 'Tienes un nuevo mensaje en la entrevisa para el trabajo ' + i.job.title, i.id)
                    n.save()
                res = {
                    'msg': 'Ok',
                    'results': MessageSchema().dump(i.messages, many=True)
                }
                return make_response(jsonify(res), 201)
            raise Forbidden('No tienes permisos para realizar esta accion.')
        raise ObjectNotFound('No existe la entrevista para el Id dado.')
            

api.add_resource(IdInterviewR, '/api/interviews/<int:id>')
api.add_resource(MessagesR, '/api/interviews/<int:id>/message')
api.add_resource(GetAllByUserR, '/api/interviews/user/<int:id>')

# ADMIN ENDPOINTS

class InterviewsGetAllRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = InterviewGetAllSchema().load(request.get_json())
        pagResult = Interview.get_pag(data)
        return makePagResponse(pagResult, InterviewGetAllResponseSchema())

class InterviewsRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        u = User.get_by_id(data['user_id'])
        if u is not None:
            j = Job.get_by_id(data['job_id'])
            if j is not None:
                i = Interview.get_by_user_and_job(u,j)
                if i is None:
                    i = Interview(user_id, u.id, j.id)
                    i.messages.append(Message(user_id, data['text']))
                    i.save()
                    n = Notification(u.id, 'Solicitud de entrevista', 'Tienes una nueva solicitud de entrevista para el trabajo ' + j.title, i.id)
                    n.save()
                    res = {
                    'msg': 'Entrevista creada.',
                    'result': InterviewSchema().dump(i)
                    }
                    return make_response(jsonify(res), 201)
                raise BadRequest('Ya existe una entrevista creada para ese usuario en ese trabajo.')
            raise ObjectNotFound('No existe el trabajo indicado.')
        raise ObjectNotFound('No existe el usuario indicado.')

class InterviewRA(Resource):
    def get(self, id):
        user_id = validateToken(request, 'funcionario')
        i = Interview.get_by_id(id)
        if i is not None:
            u = i.user
            for m in i.messages:
                if m.created_by == u.id:
                    m.status = 'readed'
            i.save()
            res = {
            'msg': 'Ok.',
            'results': interview_schema.dump(i)
            }
            return make_response(jsonify(res), 200)
        raise ObjectNotFound('No existe la entrevista para el Id dado.')

    def put(self, id):
        user_id = validateToken(request, 'funcionario')
        i = Interview.get_by_id(id)
        if i is not None:
            data = request.get_json()
            try:
                iSchema = interview_put_schema.load(data)
                if 'date_interview' in iSchema:
                    i.date_interview = iSchema['date_interview']
                if 'status' in iSchema:
                    i.status = iSchema['status']
                if 'results' in iSchema:
                    i.results = iSchema['results']
                i.save()
                res = {
                'msg': 'Ok.',
                'results': interview_schema.dump(i)
                }
                return make_response(jsonify(res), 200)
            except ValidationError as e:
                raise BadRequest('Error en los campos enviados.')
        raise ObjectNotFound('No existe la entrevista para el Id dado.')


api.add_resource(InterviewsGetAllRA, '/api/interviews/a/getall')
api.add_resource(InterviewsRA, '/api/interviews/a')
api.add_resource(InterviewRA, '/api/interviews/a/<int:id>')
