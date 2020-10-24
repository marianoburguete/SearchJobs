from app.database.db import db, BaseModelMixin

class Curriculum(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    birth_date = db.Column(db.Integer) #esto tiene que se un datetime, lo dejo asi para probar
    phone = db.Column(db.Integer)
    country = db.Column(db.String)
    address = db.Column(db.String)
    avatar = db.Column(db.String)
    description = db.Column(db.String)
    education = db.relationship('Education', backref='curriculum', lazy=False, cascade='all, delete-orphan')
    workexperience = db.relationship('WorkExperience', backref='curriculum', lazy=False, cascade='all, delete-orphan')
    languages = db.relationship('Language', backref='curriculum', lazy=False, cascade='all, delete-orphan')
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name):
        self.name = name