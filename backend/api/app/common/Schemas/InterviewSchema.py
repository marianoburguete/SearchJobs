from marshmallow import fields

from .MessageSchema import MessageSchema

from app.ext import ma


class InterviewSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date_interview = fields.DateTime()
    status = fields.String()
    results = fields.String()
    created_by = fields.Integer()
    user = fields.Nested('InterviewUserGetAllSchema', many=False)
    job = fields.Nested('InterviewJobGetAllSchema', many=False)
    messages = fields.Nested('MessageSchema', many=True)

class InterviewGetAllResponseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date_interview = fields.DateTime()
    status = fields.String()
    results = fields.String()
    created_by = fields.Integer()
    user = fields.Nested('InterviewUserGetAllSchema', many=False)
    job = fields.Nested('InterviewJobGetAllSchema', many=False)
    messages = fields.Nested('MessageSchema', many=True)
    created_at = fields.DateTime()

class InterviewUserGetAllSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String()

class InterviewJobGetAllSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()

class InterviewGetUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date_interview = fields.DateTime()
    status = fields.String()
    job = fields.Nested('InterviewJobGetAllSchema', many=False)
    messages = fields.Nested('MessageSchema', many=True)

class InterviewPutSchema(ma.Schema):
    id = fields.Integer()
    date_interview = fields.DateTime()
    status = fields.String(required=True)
    results = fields.String(allow_none=True)

# INPUT

class InterviewGetAllSchema(ma.Schema):
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)
    status = fields.String(required=True)
    user = fields.Integer()
    job = fields.Integer()
    unread = fields.Boolean()