from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from marshmallow import ValidationError

from ..common.Schemas.CompanySchema import CompanySchema, CompanyGetAllResponseSchema, CompanyGetAllSchema, CompanySearchResultsSchema
from ..common.Schemas.CommentarySchema import CommentarySchema
from ..database.JobModel import Job
from ..database.UserModel import User
from ..database.InterviewModel import Interview
from ..database.MessageModel import Message
from ..database.CommentaryModel import Commentary
from ..database.CompanyModel import Company
from ..database.RequirementModel import Requirement
from ..database.ApplicationModel import Application
from ..database.NotificationModel import Notification
from ..database.SearchModel import Search

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
        if data is None:
            raise BadRequest('No se encontraron los filtros.')
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

class CompaniesSearchR(Resource):
    def post(self):
        data = request.get_json()
        if data is None:
            raise BadRequest('No se encontraron los filtros.')
        pagResult = Company.get_pag(data)
        s = Search(data['search'], None)
        s.save()
        return makePagResponse(pagResult, CompanySearchResultsSchema())

class CommentariesR(Resource):
    def post(self, id):
        user_id = validateToken(request, 'cliente')
        c = Company.get_by_id(id)
        if c is not None:
            u = User.get_by_id(user_id)
            if u is not None:
                c.commentaries.append(Commentary(user_id, request.get_json()['text']))
                c.save()
                res = {
                    'msg': 'Ok',
                    'results': CommentarySchema().dump(c.commentaries, many=True)
                }
                return make_response(jsonify(res), 201)
            raise Forbidden('No tienes permisos para realizar esta accion.')
        raise ObjectNotFound('No existe la empresa para el Id dado.')

api.add_resource(CompaniesGetAllRA, '/api/companies/a/getall')
api.add_resource(CompanyRA, '/api/companies/a/<int:id>')
api.add_resource(CompaniesSearchR, '/api/companies/search')
api.add_resource(CommentariesR, '/api/companies/<int:id>/commentary')
