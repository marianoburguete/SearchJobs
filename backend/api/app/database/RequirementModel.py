from app.database.db import db, BaseModelMixin

class Requirement(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    def __init__(self, info):
        self.info = info