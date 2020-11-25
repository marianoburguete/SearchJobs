from app.database.db import db, BaseModelMixin
from datetime import datetime

class Curriculum(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.DateTime)
    phone = db.Column(db.String)
    country = db.Column(db.String)
    address = db.Column(db.String)
    avatar = db.Column(db.String)
    description = db.Column(db.String)
    education = db.relationship('Education', backref='curriculum', lazy=False, cascade='all, delete-orphan')
    workexperience = db.relationship('WorkExperience', backref='curriculum', lazy=False, cascade='all, delete-orphan')
    languages = db.relationship('Language', backref='curriculum', lazy=False, cascade='all, delete-orphan')
    categories = db.relationship('Curriculum_Category')
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_user_id(cls, id):
        return cls.query.filter(cls.user_id==id).first()
    
    @classmethod
    def get_all_by_job_id(cls, id):
        res = db.engine.execute('select distinct u.* from "user" as u, job as j, curriculum as c, category as cat, subcategory as sc, curriculum__category as cc where j.id = ' + str(id) + ' and j.subcategory_id = sc.id and cc.category_id = sc.category_id and cc.curriculum_id = c.id and u.id = c.user_id')
        return [row for row in res]
    
    @classmethod
    def get_all_recommended_users_by_filters(cls, data):
        sqlQueryString = 'select distinct u.* from "user" as u, curriculum as c, category as cat, curriculum__category as cc, language as l where u."role" = ' + "'cliente' and c.user_id = u.id"

        if 'category' in data['filters'] and data['filters']['category'] is not None:
            sqlQueryString += ' and cc.curriculum_id = c.id and u.id = c.user_id and cat.id = ' + str(data['filters']['category']) + ' and cc.category_id = cat.id'
        
        if 'language' in data['filters'] and data['filters']['language'] is not None and data['filters']['language'][0] != '' and data['filters']['language'][0] != ' ':
            sqlQueryString += " and l.name = '" + data['filters']['language'] + "' and l.curriculum_id = c.id"
        
        if 'ageRange' in data['filters'] and data['filters']['ageRange'] is not None:
            if 'maxAge' in data['filters']['ageRange'] and data['filters']['ageRange']['maxAge']:
                sqlQueryString += " and DATE_PART('year', now()::date) - DATE_PART('year', c.birth_date::date) <= " + str(data['filters']['ageRange']['maxAge'])
            if 'minAge' in data['filters']['ageRange'] and data['filters']['ageRange']['minAge']:
                sqlQueryString += " and DATE_PART('year', now()::date) - DATE_PART('year', c.birth_date::date) >= " + str(data['filters']['ageRange']['minAge'])

        sqlQueryString += ';'
        print(sqlQueryString)
        res = db.engine.execute(sqlQueryString)
        return [row for row in res]