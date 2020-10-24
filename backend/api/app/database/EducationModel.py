from app.database.db import db, BaseModelMixin

class Education(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    place = db.Column(db.String)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

    curriculum_id = db.Column(db.Integer, db.ForeignKey('curriculum.id'), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name):
        self.name = name