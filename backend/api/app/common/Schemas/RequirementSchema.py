from marshmallow import fields

from app.ext import ma


class RequirementSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    info = fields.String()
    job_id = fields.Integer()