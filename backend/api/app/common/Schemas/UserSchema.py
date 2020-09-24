from marshmallow import fields

from app.ext import ma

from app.common.Schemas.CurriculumSchema import CurriculumSchema
from app.common.Schemas.ApplicationSchema import ApplicationSchema
from app.common.Schemas.RatingSchema import RatingSchema
from app.common.Schemas.NotificationSchema import NotificationSchema
from app.common.Schemas.MessageSchema import MessageSchema

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    email = fields.String()
    password = fields.String()
    role = fields.String()
    phone = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    created_at = fields.DateTime()
    curriculum = fields.Nested('CurriculumSchema', many=True)
    applications = fields.Nested('ApplicationSchema', many=True)
    ratings = fields.Nested('RatingSchema', many=True)
    notifications = fields.Nested('NotificationSchema', many=True)
    messages = fields.Nested('MessageSchema', many=True)