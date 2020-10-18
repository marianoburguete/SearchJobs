from marshmallow import fields

from app.ext import ma

class ApplicationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String()
    job_id = fields.Integer()
    user_id = fields.Integer()
    created_at = fields.DateTime()

class ApplicationListSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String()
    job = fields.Nested('ApplicationListJobSchema', many=False)
    user = fields.Nested('ApplicationListUserSchema', many=False)
    created_at = fields.DateTime()

class ApplicationListUserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String()

class ApplicationListJobSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()


# Input

class ApplicationSearchParametersSchema(ma.Schema):
    page = fields.Integer(required=True)
    per_page = fields.Integer(required=True)
    status = fields.String(required=True)
    user = fields.Integer()
    job = fields.Integer()