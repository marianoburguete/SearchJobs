from app.database.db import db, BaseModelMixin
from datetime import datetime

class Category(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    jobs = db.relationship('Job', backref='category', lazy=False, cascade='all, delete-orphan')
    subcategories = db.relationship('Subcategory', backref='category', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name):
        self.name = name