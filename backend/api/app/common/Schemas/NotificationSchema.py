from marshmallow import fields

from app.ext import ma

class NotificationSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String()
    title = fields.String()
    description = fields.String()
    user_id = fields.Integer()
    created_at = fields.DateTime()