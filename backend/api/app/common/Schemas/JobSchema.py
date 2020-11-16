from marshmallow import fields

from app.ext import ma

from app.common.Schemas.RequirementSchema import RequirementSchema
from app.common.Schemas.ApplicationSchema import ApplicationSchema
from app.common.Schemas.InterviewSchema import InterviewSchema



class JobSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    url = fields.String()
    title = fields.String()
    location = fields.String()
    workday = fields.String()
    contract_type = fields.String()
    salary = fields.Integer()
    description = fields.String()
    company_id = fields.String()
    requirements = fields.Nested('RequirementSchema', many=True)
    applications = fields.Nested('ApplicationSchema', many=True)
    interviews = fields.Nested('InterviewSchema', many=True)
    #subcategory = fields.Nested('Job_SubcategorySchema')
    active = fields.Boolean()

class JobDetailsSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    location = fields.String()
    workday = fields.String()
    contract_type = fields.String()
    salary = fields.Integer()
    description = fields.String()
    company = fields.Nested('JobSearchCompanyInfoSchema')
    requirements = fields.Nested('RequirementSchema', many=True)
    #subcategory = fields.Nested('Job_SubcategorySchema')
    created_at = fields.DateTime()
    active = fields.Boolean()


class JobSearchResultsSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    location = fields.String()
    created_at = fields.DateTime()
    company = fields.Nested('JobSearchCompanyInfoSchema')
    active = fields.Boolean()


class JobSearchCompanyInfoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    logo = fields.String()

class JobsByTitleSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()

class Job_SubcategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    category = fields.Nested('Job_CategorySchema')

class Job_CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()