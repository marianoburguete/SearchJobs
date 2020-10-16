from marshmallow import fields

#from .UserSchema import UserSchema

from app.ext import ma

class MessageSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String()
    text = fields.String()
    created_by = fields.Integer()
    to_interview = fields.Integer()

    created_at = fields.DateTime()
    read_at = fields.DateTime()