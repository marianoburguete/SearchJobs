from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from marshmallow import ValidationError

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema
from ..common.Schemas.CompanySchema import CompanySchema, CompanyGetAllResponseSchema, CompanyGetAllSchema
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

companies_bp = Blueprint('companies_bp', __name__)
company_schema = CompanySchema()
api = Api(companies_bp)

class CompaniesGetAllRA(Resource):
    def post(self):
        data = request.get_json()
        pagResult = Company.get_pag(data)
        return makePagResponse(pagResult, CompanyGetAllResponseSchema())

class CompanyRA(Resource):
    def get(self, id):
        c = Company.get_by_id(id)
        if c is not None:
            res = {
            'msg': 'Ok.',
            'results': company_schema.dump(c)
            }
            return make_response(jsonify(res), 200)
        raise ObjectNotFound('No existe la empresa para el Id dado.')

api.add_resource(CompaniesGetAllRA, '/api/companies/a/getall')
api.add_resource(CompanyRA, '/api/companies/a/<int:id>')
