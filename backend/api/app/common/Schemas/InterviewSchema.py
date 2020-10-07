from marshmallow import fields

from .MessageSchema import MessageSchema

from app.ext import ma


class InterviewSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date_interview = fields.DateTime()
    status = fields.String()
    results = fields.String()
    created_by = fields.Integer()
    to_user = fields.Integer()
    to_job = fields.Integer()
    messages = fields.Nested('MessageSchema', many=True)

class InterviewGetUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date_interview = fields.DateTime()
    to_job = fields.Integer()
    messages = fields.Nested('MessageSchema', many=True)

class InterviewPutSchema(ma.Schema):
    date_interview = fields.DateTime()
    status = fields.String(required=True)
    results = fields.String()