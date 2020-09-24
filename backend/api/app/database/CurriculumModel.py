from app.database.db import db, BaseModelMixin

class Curriculum(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Integer) #esto tiene que se un datetime, lo dejo asi para probar
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date