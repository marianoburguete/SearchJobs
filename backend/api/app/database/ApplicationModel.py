from app.database.db import db, BaseModelMixin
from datetime import datetime


class Application(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False, default='created')
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id):
        self.user_id = user_id