from app.database.db import db, BaseModelMixin
from datetime import datetime


class Interview(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_interview = db.Column(db.DateTime)
    #Los 4 estados van a ser: created, accepted, finished, cancelled
    status = db.Column(db.String, nullable=False, default='created')
    #las anotaciones que haga el entrevistador
    results = db.Column(db.String)
    # created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_job = db.Column(db.Integer, db.ForeignKey('job.id'))
    messages = db.relationship(
        'Message', backref='interview', lazy=False, cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, created_by, to_user, to_job):
        self.created_by = created_by
        self.to_user = to_user
        self.to_job = to_job

    @classmethod
    def get_by_user_and_job(cls, user, job):
        return cls.query.filter(cls.to_user == user.id, cls.to_job == job.id).first()