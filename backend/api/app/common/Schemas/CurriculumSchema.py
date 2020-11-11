from marshmallow import fields

from app.ext import ma


class CurriculumSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    birth_date = fields.DateTime(required=True)
    phone = fields.String(required=True)
    country = fields.String(required=True)
    address = fields.String(required=True)
    avatar = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    education = fields.Nested('EducationSchema', many=True, allow_none=True)
    workexperience = fields.Nested('WorkExperienceSchema', many=True, allow_none=True)
    languages = fields.Nested('LanguageSchema', many=True, allow_none=True)
    user = fields.Nested('CurriculumUserSchema', allow_none=True)
    categories = fields.Nested('CategoriesUserSchema', many=True, allow_none=True)

class EducationSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    place = fields.String()
    start_date =fields.DateTime()
    end_date = fields.DateTime(allow_none=True)

class WorkExperienceSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()
    ocupation = fields.String()
    start_date = fields.DateTime()
    end_date = fields.DateTime(allow_none=True)

class LanguageSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()

class CurriculumUserSchema(ma.Schema):
    id = fields.Integer()
    email = fields.String()

class CategoriesUserSchema(ma.Schema):
    category = fields.Nested('CategoryUserSchema', allow_none=True)
    
class CategoryUserSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String()