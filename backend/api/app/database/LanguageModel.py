from app.database.db import db, BaseModelMixin

class Language(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    curriculum_id = db.Column(db.Integer, db.ForeignKey('curriculum.id'), nullable=False)

    def __init__(self, name):
        self.name = name