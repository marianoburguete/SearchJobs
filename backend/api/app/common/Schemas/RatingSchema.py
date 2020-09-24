from marshmallow import fields

from app.ext import ma

class RatingSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    description = fields.String()
    score = fields.Integer()
    user_id = fields.Integer()
    company_id = fields.Integer()
    created_at = fields.DateTime()