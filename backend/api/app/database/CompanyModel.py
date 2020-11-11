from app.database.db import db, BaseModelMixin

class Company(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    info = db.Column(db.String)
    logo = db.Column(db.String)
    jobs = db.relationship('Job', backref='company', lazy=False, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='company', lazy=False)
    commentaries = db.relationship('Commentary', backref='company', lazy=False)
    
    def __init__(self, name):
        self.name = name

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter(Company.name==name).first()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(Company.id==id).first()

    @classmethod
    def get_pag(cls, data):
        filtro = cls.query

        if 'search' in data and data['search'] is not None:
            filtro = filtro.filter(db.or_(Company.name.contains(data['search'].strip())))

        if 'page' in data and 'per_page' in data:
            return filtro.paginate(int(data['page']), int(data['per_page']), False, 40)
        else:
            return filtro.paginate(1, 10, False)
