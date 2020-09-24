from marshmallow import fields

from app.ext import ma


class CompanySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date_interview = fields.DateTime()
    status = fields.String()
    description = fields.String()
    results = fields.String()
    created_by = fields.Integer()
    to_user = fields.Integer()