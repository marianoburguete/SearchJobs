from app.database.db import db, BaseModelMixin
from datetime import datetime


class Message(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False, default='unread')
    title = db.Column(db.String)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    user_question_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_answer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self):
        self.created_at = datetime.utcnow