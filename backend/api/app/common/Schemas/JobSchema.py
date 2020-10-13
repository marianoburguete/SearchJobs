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
    created_at = fields.DateTime()

class JobSearchResultsSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    location = fields.String()
    created_at = fields.DateTime()
    company = fields.Nested('JobSearchCompanyInfoSchema')


class JobSearchCompanyInfoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    logo = fields.String()