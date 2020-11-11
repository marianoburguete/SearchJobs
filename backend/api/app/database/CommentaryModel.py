from app.database.db import db, BaseModelMixin
from datetime import datetime

class Commentary(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, created_by, text):
        self.created_by = created_by
        self.text = text