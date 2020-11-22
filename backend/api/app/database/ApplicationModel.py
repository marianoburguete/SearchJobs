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

    @classmethod
    def get_pag(cls, data):
        filtro = cls.query

        filtro = filtro.filter(cls.status == data['status'])
        
        if 'user' in data:
            filtro = filtro.filter(cls.user_id == data['user'])
        
        if 'job' in data:
            filtro = filtro.filter(cls.job_id == data['job'])

        filtro = filtro.order_by(cls.created_at.desc())

        if 'page' in data and 'per_page' in data:
            return filtro.paginate(int(data['page']), int(data['per_page']), False, 40)
        else:
            return filtro.paginate(1, 10, False)
    
    @classmethod
    def get_by_user_and_job(cls, user_id, job_id):
        filtro = cls.query
        filtro = filtro.filter(cls.user_id == user_id)
        filtro = filtro.filter(cls.job_id == job_id)
        return filtro.first()