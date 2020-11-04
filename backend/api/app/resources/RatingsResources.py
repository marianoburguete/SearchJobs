from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from marshmallow import ValidationError

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema
from ..common.Schemas.InterviewSchema import InterviewSchema, InterviewGetUserSchema, InterviewPutSchema, InterviewGetAllSchema, InterviewGetAllResponseSchema
from ..common.Schemas.CompanySchema import CompanySchema
from ..common.Schemas.CompanySchema import CompanyGetAllSchema 
from ..common.Schemas.RatingSchema import RatingSchema
from ..common.Schemas.MessageSchema import MessageSchema
from ..database.JobModel import Job
from ..database.UserModel import User
from ..database.InterviewModel import Interview
from ..database.MessageModel import Message
from ..database.CompanyModel import Company
from ..database.RatingModel import Rating
from ..database.RequirementModel import Requirement
from ..database.ApplicationModel import Application
from ..database.NotificationModel import Notification

from ..common.error_handling import ObjectNotFound, BadRequest, Forbidden
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json
from datetime import datetime

rating_bp = Blueprint('ratings_bp', __name__)
rating_schema = RatingSchema()
api = Api(rating_bp)

class RatingsGetAllRA(Resource):
    def post(self):
        data = CompanyGetAllSchema().load(request.get_json())
        pagResult = Interview.get_pag(data)
        return makePagResponse(pagResult, InterviewGetAllResponseSchema())

class RatingRA(Resource):
    def get(self, id):
        r = Rating.get_by_id(id)
        if r is not None:
            res = {
            'msg': 'Ok.',
            'results': rating_schema.dump(r)
            }
            return make_response(jsonify(res), 200)
        raise ObjectNotFound('No existe la puntuacion de empresa para el Id dado.')

        def post(self, id):
            user_id = validateToken(request, 'cliente')
            

api.add_resource(RatingsGetAllRA, '/api/ratings/a/getall')
api.add_resource(RatingRA, '/api/ratings/a/<int:id>')
