from app.database.db import db, BaseModelMixin
from datetime import datetime


class Notification(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False, default='unread')
    title = db.Column(db.String)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, title, description):
        self.user_id = user_id
        self.title = title
        self.description = description

    @classmethod
    def get_pag(cls, data, id):
        return cls.query.filter(cls.user_id == id).order_by(cls.created_at.desc()).paginate(data['page'], 10, False)

    @classmethod
    def unreadNotificationsCount(cls, id):
        return cls.query.filter(cls.user_id == id, cls.status == 'unread').count()