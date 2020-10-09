from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema, JobDetailsSchema
from ..common.Schemas.ApplicationSchema import ApplicationSchema
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
        if j is not None:
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


api.add_resource(ApplicationR, '/api/application')



# ADMIN ENDPOINTS


class ApplicationsRA(Resource):
    def get(self):
        user_id = validateToken(request, 'funcionario')
        data = {
            'page': request.args['page'],
            'per_page': request.args['per_page']
        }
        pagResult = Application.get_pag(data)
        return makePagResponse(pagResult, ApplicationSchema())


api.add_resource(ApplicationsRA, '/api/applications/a')