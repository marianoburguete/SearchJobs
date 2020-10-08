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

        # if 'search' in data and data['search'] is not None:
        #     filtro = filtro.filter(db.or_(Job.title.contains(data['search']),
        #                                   Job.description.contains(data['search'])))

        # if 'workday' in data and data['workday'] is not None:
        #     filtro = filtro.filter(Job.workday == data['workday'])

        if 'page' in data and 'per_page' in data:
            return filtro.paginate(int(data['page']), int(data['per_page']), False, 40)
        else:
            return filtro.paginate(1, 10, False)