from app.database.db import db, BaseModelMixin
from datetime import datetime


class Message(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False, default='unread')
    text = db.Column(db.String)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_interview = db.Column(db.Integer, db.ForeignKey('interview.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)

    def __init__(self, created_by, text):
        self.created_by = created_by
        self.text = text