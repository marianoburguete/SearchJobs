from app.database.db import db, BaseModelMixin
from datetime import datetime


class Rating(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
