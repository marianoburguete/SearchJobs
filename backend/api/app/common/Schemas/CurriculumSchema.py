from marshmallow import fields

from app.ext import ma


class CurriculumSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    birth_date = fields.Integer()
    user_id = fields.Integer()