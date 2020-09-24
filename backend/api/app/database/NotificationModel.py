from app.database.db import db, BaseModelMixin
from datetime import datetime


class Notification(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False, default='unread')
    title = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self):
        self.created_at = datetime.utcnow