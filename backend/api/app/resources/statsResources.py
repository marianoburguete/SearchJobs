from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.StatSchema import jobsPerCategorySchema, applicationsXInterviewsSchema, popularSearchesSchema
from ..database.StatsQuery import jobsPerCategoryStats, postulationsXInterviewsStats, popularSearches

from ..common.error_handling import ObjectNotFound, BadRequest


stats_bp = Blueprint('stats_bp', __name__)

api = Api(stats_bp)


class StatsR(Resource):
    def get(self):
        j = jobsPerCategoryStats()
        oka = postulationsXInterviewsStats()
        ps = popularSearches()
        res = {
            'msg': 'Ok',
            'results': {
                'jobsPerCategoryCount': jobsPerCategorySchema().dump(j, many=True),
                'applicationsXInterviews': applicationsXInterviewsSchema().dump(oka, many=True),
                'popularSearches': popularSearchesSchema().dump(ps, many=True)
            }
        }
        return make_response(jsonify(res), 200)


        
api.add_resource(StatsR, '/api/stats')