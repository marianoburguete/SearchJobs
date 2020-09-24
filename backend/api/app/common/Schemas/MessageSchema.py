from marshmallow import fields

from app.ext import ma

class MessageSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    status = fields.String()
    title = fields.String()
    question = fields.String()
    answer = fields.String()
    user_question_id = fields.Integer()
    user_answer_id = fields.Integer()
    created_at = fields.DateTime()