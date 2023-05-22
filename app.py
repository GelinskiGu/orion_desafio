from flask import Flask, render_template, redirect, url_for, flash, request  # noqa: F401, E501
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin  # noqa: F401, E501
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField  # noqa: F401, E501
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo  # noqa: F401, E501
from flask_wtf import FlaskForm
from sqlalchemy import create_engine, LargeBinary, Integer, String, ForeignKey, DateTime, func, Column  # noqa: F401, E501
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class, UploadNotAllowed  # noqa: F401, E501
from datetime import datetime  # noqa: F401, E501
import os
from sqlalchemy.exc import SQLAlchemyError


basedir = os.path.abspath(os.path.dirname(__file__))
path = './assets/recipes_images'

# Configuracao banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8rPTT7k#gT@localhost/orion'  # noqa: E501
app.config['SECRET_KEY'] = 'qTUL^P3cQ%'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(
    basedir, path)

bcrypt = Bcrypt(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

Session = sessionmaker(bind=engine)
session = Session()

db = SQLAlchemy(app, session_options={"autocommit": False})  # noqa: F811

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(LargeBinary, nullable=False)
    name = Column(String(255), nullable=False)

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


"""
    def save_image(self, image):
        print("Imagem sendo salva")
        now = datetime.now()
        folder = f"assets/recipes_images/{now.year}/{now.strftime('%m')}"
        filename = photos.save(image, folder=folder)
        self.image_filename = filename
        self.image_path = photos.path(filename)
        session.commit()
"""


@login_manager.user_loader
def load_user(user_id):
    return session.get(User, user_id)


# Formulário de cadastro
class RegisterForm(FlaskForm):
    # Validações para o form de cadastro
    username = StringField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Nome de usuário"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=20)], render_kw={"placeholder": "Senha"})
    repeat_password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=20)],
        render_kw={"placeholder": "Repita sua senha"})
    name = StringField(validators=[InputRequired(), Length(
        min=8, max=255)], render_kw={"placeholder": "Nome Completo"})
    submit = SubmitField('Register')

    # Checagem para não existir usuários com mesmo username
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'Nome de usuário já existe. Favor escolher um nome diferente.')

    def validate_repeat_password(self, repeat_password):
        if repeat_password.data != self.password.data:
            raise ValidationError('As senhas não conferem.')

# Formulário de login


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=5, max=20)], render_kw={"placeholder": "Nome de usuário"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=8, max=20)], render_kw={"placeholder": "Senha"})
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Usuário não existe.')
        else:
            return True

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        print(bcrypt.generate_password_hash(password.data))
        if user and not bcrypt.check_password_hash(user.password, password.data):  # noqa: E501
            raise ValidationError('Senha incorreta.')


class NewRecipeForm(FlaskForm):
    title = TextAreaField(validators=[InputRequired(), Length(max=255)],
                          render_kw={"placeholder": "Título de sua receita"})
    category = SelectField('Categoria', coerce=int)
    description = TextAreaField(validators=[InputRequired()],
                                render_kw={"placeholder": "Descrição de sua receita"})  # noqa: E501
    ingredients = TextAreaField(validators=[InputRequired()],
                                render_kw={"placeholder": "Ingredientes de sua receita"})  # noqa: E501
    preparation_steps = TextAreaField(validators=[InputRequired()],
                                      render_kw={"placeholder": "Qual o passo-a-passo de sua receita?"})  # noqa: E501
    image_filename = FileField(description="Coloque sua imagem da receita")
    submit = SubmitField('Cadastrar')


"""
categories = [
    Category(name='Café'),
    Category(name='Salgados'),
    Category(name='Doces'),
    Category(name='Bolos'),
    Category(name='Tortas')
]
session.add_all(categories)
session.commit()
"""


@app.route("/")
def home():
    recipes = session.query(Recipe).order_by(
            Recipe.created_at.asc()).all()
    return render_template("home.html", recipes=recipes)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, name=form.name.data)  # noqa: E501
        print("Usuário criado.")
        session.add(new_user)
        session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                print("Usuário logado")
                return redirect(url_for('home'))

    return render_template("login.html", form=form)


@app.route('/new_recipe', methods=['GET', 'POST'])
def register_new_recipe():
    form = NewRecipeForm()

    if current_user.is_authenticated:
        # Usuário está logado
        categories = session.query(Category).order_by(
            Category.name.asc()).all()
        form.category.choices = [(category.id, category.name)
                                 for category in categories]
        print(form.category.choices)
        print(form.title.data, form.category.data, form.description.data,
              form.ingredients.data, form.preparation_steps.data,
              form.image_filename.data)
        if form.validate_on_submit():
            print("Validado.")
            now = datetime.now()
            path_image = f"{now.year}/{now.strftime('%m')}"
            try:
                filename = photos.save(
                    form.image_filename.data, folder=path_image)
                file_url = photos.url(filename)
            except UploadNotAllowed:
                flash("Ocorreu um erro para o salvamento da imagem.", "error")
                return redirect(url_for("register_new_recipe"))
            print(form.image_filename.data.filename)
            recipe = Recipe(author=current_user.id,
                            category_id=form.category.data,
                            title=form.title.data,
                            description=form.description.data,
                            ingredients=form.ingredients.data,
                            preparation_steps=form.preparation_steps.data,
                            image_filename=form.image_filename.data.filename,
                            image_path=file_url
                            )  # noqa: E501
            try:
                session.add(recipe)
                session.commit()
                flash("Receita cadastrada com sucesso!", "message")
                return redirect(url_for("home"))
            except SQLAlchemyError:
                flash("Ocorreu um erro para cadastrar receita.", "error")
                session.rollback()
                return redirect(url_for("register_new_recipe"))

    else:
        # Usuário não logado
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))

    return render_template("new_recipe.html", form=form)


"""
Para testar qualquer html que estiver fazendo, é só tirar o comentário desse trecho de código. # noqa: E501
No lugar de "teste.html", colocar nome do arquivo .html que estiver localizado na pasta templates.
Na url, colocar http://127.0.0.1:5000/teste

@app.route("/teste")
def hello_world():
    return render_template("teste.html")
"""


if __name__ == '__main__':
    app.run(debug=True)
