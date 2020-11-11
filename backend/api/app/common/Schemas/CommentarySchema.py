from marshmallow import fields
from app.ext import ma

class CommentarySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    text = fields.String()
    created_by = fields.Integer()
    created_at = fields.DateTime()
    company_id = fields.Integer()