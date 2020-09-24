from marshmallow import fields

from app.ext import ma

from app.common.Schemas.JobSchema import JobSchema
from app.common.Schemas.RatingSchema import RatingSchema

class CompanySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    info = fields.String()
    jobs = fields.Nested('JobSchema', many=True)
    ratings = fields.Nested('RatingSchema', many=True)