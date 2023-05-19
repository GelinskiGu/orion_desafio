from sqlalchemy import LargeBinary
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES
from datetime import datetime

db = SQLAlchemy()


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


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship("Category")
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String, nullable=True)
    ingredients = db.Column(db.String, nullable=True)
    preparation_steps = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    image_filename = db.Column(db.String, nullable=True)
    image_path = db.Column(db.String, nullable=True)
