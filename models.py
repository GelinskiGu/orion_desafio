from sqlalchemy import LargeBinary
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(LargeBinary, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
