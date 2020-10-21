from app.database.db import db, BaseModelMixin
from datetime import datetime

class Subcategory(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    jobs = db.relationship('Job', backref='subcategory', lazy=False, cascade='all, delete-orphan')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    @classmethod
    def getByName(cls, name):
        return cls.query.filter(cls.name == name).first()