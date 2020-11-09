from app.database.db import db, BaseModelMixin
from datetime import datetime

class Curriculum_Category(db.Model, BaseModelMixin):
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    curriculum_id = db.Column(db.Integer, db.ForeignKey('curriculum.id'), primary_key=True)
    category = db.relationship("Category")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self):
        pass