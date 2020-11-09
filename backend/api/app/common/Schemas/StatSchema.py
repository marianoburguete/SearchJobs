from marshmallow import fields

from app.ext import ma


class jobsPerCategorySchema(ma.Schema):
    value = fields.Integer()
    name = fields.String()

class applicationsXInterviewsSchema(ma.Schema):
    day = fields.Date()
    applications = fields.Integer()
    interviews = fields.Integer()

class popularSearchesSchema(ma.Schema):
    text = fields.String()
    count = fields.Integer()