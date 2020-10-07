from app.database.db import db, BaseModelMixin
from datetime import datetime
from ..common.error_handling import ObjectNotFound


class Job(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    workday = db.Column(db.String)
    contract_type = db.Column(db.String)
    salary = db.Column(db.String)
    description = db.Column(db.String)
    requirements = db.relationship(
        'Requirement', backref='job', lazy=False, cascade='all, delete-orphan')
    applications = db.relationship(
        'Application', backref='job', lazy=False, cascade='all, delete-orphan')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    interviews = db.relationship('Interview', backref='job', lazy=False, cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, url, title):
        self.url = url
        self.title = title

    @classmethod
    def get_pag(cls, data):
        filtro = cls.query

        if 'search' in data and data['search'] is not None:
            filtro = filtro.filter(db.or_(Job.title.contains(data['search']),
                                          Job.description.contains(data['search'])))

        if 'workday' in data and data['workday'] is not None:
            filtro = filtro.filter(Job.workday == data['workday'])

        if 'page' in data and 'per_page' in data:
            return filtro.paginate(data['page'], data['per_page'], False, 40)
        else:
            return filtro.paginate(1, 10, False)
