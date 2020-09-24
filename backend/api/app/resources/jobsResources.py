from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource

from ..common.Schemas.JobSchema import JobSchema
from ..database.JobModel import Job
from ..database.CompanyModel import Company
from ..database.RequirementModel import Requirement

from ..common.error_handling import ObjectNotFound, BadRequest
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json

jobs_bp = Blueprint('jobs_bp', __name__)

job_schema = JobSchema()

api = Api(jobs_bp)


class JobsResource(Resource):
    def get(self):
        pass

    #La peticion deberia llegar desde Scrapy
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        for job in data:
            j = Job(job['url'], job['title'])
            j.location = job['location']
            j.workday = job['workday']
            j.contract_type = job['contract_type']
            j.salary = job['salary']
            j.description = job['description']
            j.save()
            for requirement in job['requirements']:
                j.requirements.append(Requirement(requirement))
            j.save()
            c = Company.get_by_name(job['company_name'])
            if c is not None:
                c.jobs.append(j)
                c.save()
            else:
                c = Company(job['company_name'])
                c.jobs.append(j)
                c.save()
            
        return "Ok", 201


class JobsSearchResource(Resource):
    def get(self):
        data = request.get_json()
        if data is None:
            raise BadRequest('Filters not found')
        pagResult = Job.get_pag(data)

        return makePagResponse(pagResult, job_schema)


api.add_resource(JobsResource, '/api/jobs/',
                 endpoint='jobs_resource')
api.add_resource(JobsSearchResource, '/api/jobs/search',
                 endpoint='jobs_search_resource')
