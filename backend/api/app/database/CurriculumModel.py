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
        res = db.engine.execute('select distinct u.* from "user" as u, job as j, curriculum as c, category as cat, subcategory as sc, curriculum__category as cc where j.id = 6173 and j.subcategory_id = sc.id and cc.category_id = sc.category_id and cc.curriculum_id = c.id and u.id = c.user_id')
        return [row for row in res]