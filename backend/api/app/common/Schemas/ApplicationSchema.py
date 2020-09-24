from marshmallow import fields

from app.ext import ma

class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String()
    job_id = fields.Integer()
    user_id = fields.Integer()
    created_at = fields.DateTime()