from app.database.db import db, BaseModelMixin

class Company(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String)
    logo = db.Column(db.String)
    jobs = db.relationship('Job', backref='company', lazy=False, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='company', lazy=False)
    
    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter(Company.name==name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(Company.id==id).first()
