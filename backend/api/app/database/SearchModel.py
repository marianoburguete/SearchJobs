from app.database.db import db, BaseModelMixin
from datetime import datetime


class Search(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, text, user_id):
        self.text = text
        self.user_id = user_id
