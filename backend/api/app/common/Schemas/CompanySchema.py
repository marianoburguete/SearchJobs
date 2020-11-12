from marshmallow import fields

from app.ext import ma

from app.common.Schemas.JobSchema import JobSchema
from app.common.Schemas.RatingSchema import RatingSchema
from app.common.Schemas.CommentarySchema import CommentarySchema

class CompanySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    info = fields.String()
    logo = fields.String()
    jobs = fields.Nested('JobSchema', many=True)
    ratings = fields.Nested('RatingSchema', many=True)
    commentaries = fields.Nested('CommentarySchema', many=True)

class CompanyGetAllResponseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    info = fields.String()
    logo = fields.String()
    jobs = fields.Nested('CompanyJobsGetAllSchema', many=True)
    #ratings = fields.Nested('CompanyRatingsGetAllSchema', many=True)

class CompanyGetAllSchema(ma.Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    # name = fields.String()
    # info = fields.String()
    # logo = fields.String()

class CompanyJobsGetAllSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    location = fields.String()
    description = fields.String()

class CompanyRatingsGetAllSchema(ma.Schema):
    id = fields.Integer(dump_only=True)

class CompanySearchResultsSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    info = fields.String()
    logo = fields.String()