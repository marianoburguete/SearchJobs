from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema, JobDetailsSchema
from ..common.Schemas.ApplicationSchema import ApplicationSchema, ApplicationListSchema, ApplicationSearchParametersSchema
from ..database.JobModel import Job
from ..database.CompanyModel import Company
from ..database.RequirementModel import Requirement
from ..database.ApplicationModel import Application

from ..common.error_handling import ObjectNotFound, BadRequest
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json

applications_bp = Blueprint('applications_bp', __name__)

job_schema = JobSchema()

api = Api(applications_bp)

class ApplicationR(Resource):
    #Este metodo devuelve true si el usuario esta postulado
    def get(self):
        user_id = validateToken(request, ['cliente', 'funcionario'])
        data = request.args
        j = Job.get_by_id(data['job_id'])
        if j is not None:
            result = True
            a = [a for a in j.applications if a.user_id == user_id]
            if a is None or a == []:
                result = False
            res = {
                'msg': 'Ok.',
                'results': result
                }
            return make_response(jsonify(res), 200)
        raise ObjectNotFound('No existe un trabajo para el Id dado.')

    def post(self):
        user_id = validateToken(request, 'cliente')
        data = request.get_json()
        j = Job.get_by_id(data['job_id'])
        if j is not None and j.active == True:
            a = [a for a in j.applications if a.user_id == user_id]
            if a is None or a == []:
                j.applications.append(Application(user_id))
                j.save()
                res = {
                'msg': 'Postulacion creada.'
                }
                return make_response(jsonify(res), 201)
            raise BadRequest('El usuario ya se postulo para este trabajo.')
        raise ObjectNotFound('No existe un trabajo para el Id dado.')

class ApplicationGetAllR(Resource):
    def post(self, id):
        user_id = validateToken(request, 'cliente')
        if user_id == id:
            data = ApplicationSearchParametersSchema().load(request.get_json())
            pagResult = Application.get_pag(data)
            return makePagResponse(pagResult, ApplicationListSchema())
        raise BadRequest('No tienes acceso aqui.')


api.add_resource(ApplicationR, '/api/application')
api.add_resource(ApplicationGetAllR, '/api/applications/user/<int:id>')



# ADMIN ENDPOINTS


class ApplicationsRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = ApplicationSearchParametersSchema().load(request.get_json())
        pagResult = Application.get_pag(data)
        return makePagResponse(pagResult, ApplicationListSchema())

class ApplicationsDismissRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        a = Application.get_by_id(request.get_json()['id'])
        a.status = 'finished'
        a.save()
        res = {
        'msg': 'Postulacion rechazada.'
        }
        return make_response(jsonify(res), 200)


api.add_resource(ApplicationsRA, '/api/applications/a')
api.add_resource(ApplicationsDismissRA, '/api/applications/a/dismiss')