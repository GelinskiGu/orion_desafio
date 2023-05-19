from sqlalchemy import LargeBinary, Integer, String, ForeignKey, DateTime, func
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES
from datetime import datetime

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(20), nullable=False, unique=True)
    password = db.Column(LargeBinary, nullable=False)
    name = db.Column(String(255), nullable=False)

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(Integer, primary_key=True)
    author = db.Column(Integer, ForeignKey('users.id'))
    category_id = db.Column(Integer, ForeignKey('categories.id'))
    category = db.relationship("Category")
    title = db.Column(String(255), nullable=False)
    description = db.Column(String, nullable=True)
    ingredients = db.Column(String, nullable=True)
    preparation_steps = db.Column(String, nullable=True)
    created_at = db.Column(DateTime, nullable=False, default=func.now())
    image_filename = db.Column(String, nullable=True)
    image_path = db.Column(String, nullable=True)

    def save_image(self, image):
        now = datetime.now()
        folder = f"assets/recipes_images/{now.year}/{now.strftime('%m')}"
        filename = photos.save(image, folder=folder)
        self.image_filename = filename
        self.image_path = photos.path(filename)
        db.session.commit()
