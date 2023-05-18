from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin  # noqa: F401, E501
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo  # noqa: F401, E501
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8rPTT7k#gT@localhost/orion_desafio'  # noqa: E501
app.config['SECRET_KEY'] = 'qTUL^P3cQ%'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password, name):
        self.username = username
        self.password = password
        self.name = name
