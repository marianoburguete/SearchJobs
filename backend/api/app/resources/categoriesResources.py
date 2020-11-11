from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.CategorySchema import CategorySchema
from ..database.CategoryModel import Category

from ..common.error_handling import ObjectNotFound, BadRequest
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json
import re

categories_bp = Blueprint('categories_bp', __name__)

api = Api(categories_bp)


class CategoriesR(Resource):
    def get(self):
        res = {
            'msg': 'Ok',
            'results': CategorySchema().dump(Category.get_all(), many=True)
        }
        return make_response(jsonify(res), 200)

        
api.add_resource(CategoriesR, '/api/categories')