from app.database.db import db, BaseModelMixin

class Interview(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    date_interview = db.Column(db.DateTime)
    #Los 4 estados van a ser: created, accepted, finished, cancelled
    status = db.Column(db.String, nullable=False, default='created')
    #la informacion que envia el que crea la entrevista al usuario
    description = db.Column(db.String)
    #las anotaciones que haga el entrevistador
    results = db.Column(db.String)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_job = db.Column(db.Integer, db.ForeignKey('job.id'))
    
    def __init__(self, date_interview, description, created_by, to_user):
        self.date_interview = date_interview
        self.description = description
        self.created_by = created_by
        self.to_user = to_user