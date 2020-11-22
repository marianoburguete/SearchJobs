from app.database.db import db, BaseModelMixin
from datetime import datetime
from ..common.error_handling import ObjectNotFound
from sqlalchemy import func

class Job(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    location = db.Column(db.String)
    workday = db.Column(db.String)
    contract_type = db.Column(db.String)
    salary = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    description = db.Column(db.String)
    requirements = db.relationship(
        'Requirement', backref='job', lazy=False, cascade='all, delete-orphan')
    applications = db.relationship(
        'Application', backref='job', lazy=False, cascade='all, delete-orphan')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    interviews = db.relationship('Interview', backref='job', lazy=False, cascade='all, delete-orphan')

    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, url, title):
        self.url = url
        self.title = title

    @classmethod
    def get_pag(cls, data):
        filtro = cls.query
        
        filtro = filtro.filter(Job.active == True)

        if 'search' in data and data['search'] is not None:
            filtro = filtro.filter(db.or_(Job.title.contains(data['search'].strip()),
                                          Job.description.contains(data['search'].strip())))

        if 'workday' in data and data['workday'] is not None:
            filtro = filtro.filter(Job.workday == data['workday'])
        
        if 'category' in data and data['category'] is not None:
            categoryId = str(data['category'])
            subcat = [row for row in db.engine.execute('select * from subcategory where subcategory.category_id = ' + categoryId)]
            filtro = filtro.filter(Job.subcategory_id == subcat[0]['id'])

        if 'minSalary' in data and data['minSalary'] is not None:
            filtro = filtro.filter(Job.salary > int(data['minSalary']))
        
        if 'location' in data and data['location'] is not None:
            if data['location'] == 'remote':
                filtro = filtro.filter(Job.location == data['location'])
            else:
                filtro = filtro.filter(func.lower(Job.location).contains(data['location'].strip().lower()))

        if 'page' in data and 'per_page' in data:
            return filtro.paginate(data['page'], data['per_page'], False, 40)
        else:
            return filtro.paginate(1, 10, False)

    @classmethod
    def get_pag_company(cls, data):
        filtro = cls.query

        if 'company_id' in data and data['company_id'] is not None:
            filtro = filtro.filter(Job.company_id == data['company_id'])

        if 'page' in data and 'per_page' in data:
            return filtro.paginate(data['page'], data['per_page'], False, 40)
        else:
            return filtro.paginate(1, 10, False)
    
    @classmethod
    def search_by_title(cls, title):
        filtro = cls.query.filter(Job.title.contains(title))
        return filtro.paginate(1, 5, False).items
    
    @classmethod
    def search_by_url(cls, url):
        filtro = cls.query.filter(Job.url == url).first()
        return filtro
    
    @classmethod
    def get_all_by_url(cls, url):
        filtro = cls.query.filter(Job.url.contains(url))
        return filtro