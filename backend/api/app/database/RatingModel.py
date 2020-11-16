from app.database.db import db, BaseModelMixin
from datetime import datetime


class Rating(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, description, score, user_id, company_id):
        self.description = description
        self.score = score
        self.user_id = user_id
        self.company_id = company_id

    @classmethod
    def get_by_user_id_company(cls, id, companyId):
        return cls.query.filter(cls.user_id == id and cls.company_id == companyId).first()
