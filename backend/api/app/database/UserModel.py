from app.database.db import db, BaseModelMixin
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import os

class User(db.Model, BaseModelMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="cliente")
    phone = db.Column(db.String(40))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    curriculum = db.relationship('Curriculum', backref='user', lazy=False, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='user', lazy=False, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=False, cascade='all, delete-orphan')
    ratings = db.relationship('Rating', backref='user', lazy=False)
    #messages = db.relationship('Message', backref='user', lazy=False, cascade='all, delete-orphan')
    interviews = db.relationship('Interview', backref='user', lazy=False, cascade='all, delete-orphan')

    #para estadisticas
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def __init__(self, email, password):
        self.email = email 
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        return Bcrypt().check_password_hash(self.password, password)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email==email).first()