from flask import Flask, render_template, redirect, url_for, flash, request, abort  # noqa: F401, E501
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
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError, OperationalError  # noqa: F401, E501
import re


basedir = os.path.abspath(os.path.dirname(__file__))
path = './static/assets/recipes_images'

# Configuracao banco de dados
app = Flask(__name__, static_folder='static', static_url_path='/static')
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
    username = StringField(label="Nome de usuário", validators=[
        InputRequired(), Length(
            min=5, max=20)],
        render_kw={"placeholder": "Nome de Usuário"})
    password = PasswordField(label="Senha", validators=[
        InputRequired(), Length(
            min=8, max=20)], render_kw={"placeholder": "Senha"})
    repeat_password = PasswordField(label="Repita sua senha",
                                    validators=[InputRequired(), Length(
                                        min=8, max=20)],
                                    render_kw={"placeholder": "Repita sua senha"})  # noqa: E501
    name = StringField(label="Nome", validators=[InputRequired(), Length(
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
    username = StringField(label="Nome de usuário", validators=[
        InputRequired(), Length(
            min=5, max=20)])
    password = PasswordField(label="Senha",
                             validators=[InputRequired(),
                                         Length(min=8, max=20)])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Usuário não existe.')
        else:
            return True

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(user.password, password.data):  # noqa: E501
            raise ValidationError('Senha incorreta.')


class RecipeForm(FlaskForm):
    title = TextAreaField(validators=[InputRequired(), Length(max=255)],
                          render_kw={"placeholder": "Título de sua receita"})
    category = SelectField('Categoria', coerce=int)
    description = TextAreaField(validators=[InputRequired()],
                                render_kw={"placeholder": "Descrição de sua receita"})  # noqa: E501
    ingredients = TextAreaField(validators=[InputRequired()],
                                render_kw={"placeholder": "Ingredientes de sua receita"})  # noqa: E501
    preparation_steps = TextAreaField(validators=[InputRequired()],
                                      render_kw={"placeholder": "Qual o passo-a-passo de sua receita?"})  # noqa: E501
    image_filename = FileField(
        validators=[InputRequired()],
        description="Coloque sua imagem da receita")
    submit = SubmitField('Cadastrar')

    def __init__(self, initial_data=None, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        if initial_data:
            self.populate_fields(initial_data)

    def populate_fields(self, data):
        self.title.data = data.get('title', '')
        self.category.data = data.get('category', '')
        self.description.data = data.get('description', '')
        self.ingredients.data = data.get('ingredients', '')
        self.preparation_steps.data = data.get('preparation_steps', '')


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
    # TODO: try except
    recipes = session.query(Recipe).order_by(
        Recipe.created_at.asc()).all()
    return render_template("home.html", recipes=recipes, request=request)


def validate_string(string):
    if re.search(r'\d', string) is not None and re.search(r'[a-zA-Z]', string) is not None and re.search(r'\W', string) is not None:  # noqa: E501
        return True
    return False


@app.route("/register", methods=['GET', 'POST'])
def register():
    # TODO: try except
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, name=form.name.data)  # noqa: E501
        session.add(new_user)
        session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # TODO: try except
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))

    return render_template("login.html", form=form)


@app.route('/new_recipe', methods=['GET', 'POST'])
def register_new_recipe():
    form = RecipeForm()

    if current_user.is_authenticated:
        # Usuário está logado
        categories = session.query(Category).order_by(
            Category.name.asc()).all()
        form.category.choices = [(category.id, category.name)
                                 for category in categories]
        if form.validate_on_submit():
            now = datetime.now()
            path_image = f"{now.year}/{now.strftime('%m')}"
            try:
                filename = photos.save(
                    form.image_filename.data, folder=path_image)
                file_url = photos.url(filename)
            except UploadNotAllowed:
                flash("Ocorreu um erro para o salvamento da imagem.", "error")
                return redirect(url_for("register_new_recipe"))
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


@app.route('/my_recipes')
def my_recipes():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))
    recipes = session.query(Recipe).filter(
        Recipe.author == current_user.id)
    return render_template("home.html", recipes=recipes, request=request)


@app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))
    # TODO: try except
    recipe = session.get(Recipe, recipe_id)
    if recipe is None:
        abort(404)

    data = {
        'title': recipe.title,
        'category': recipe.category,
        'description': recipe.description,
        'ingredients': recipe.ingredients,
        'preparation_steps': recipe.preparation_steps,
        'image_filename': recipe.image_filename
    }
    form = RecipeForm(initial_data=data)
    categories = session.query(Category).order_by(
        Category.name.asc()).all()

    # TODO: Transformar em um set para deixar
    # como primeira a categoria selecionada.
    form.category.choices = [(category.id, category.name)
                             for category in categories]

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.category_id = form.category.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.preparation_steps = form.preparation_steps.data
        recipe.image_filename = form.image_filename.data.filename
        try:
            session.commit()
            flash("Receita atualizada com sucesso!", "message")
            return redirect(url_for("home"))
        except SQLAlchemyError:
            flash("Ocorreu um erro para atualizar receita.", "error")
            session.rollback()
            return redirect(url_for("home"))

    return render_template("edit_recipe.html", form=form, recipe=recipe)


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))

    recipe = session.get(Recipe, recipe_id)
    if recipe:
        try:
            session.delete(recipe)
            session.commit()
            flash("Receita deletada com sucesso!", "success")
            return redirect(url_for("home"))
        except InvalidRequestError as e:
            print("Erro de solicitação inválida:", str(e))
            flash("Ocorreu um erro para deletar receita.", "error")
            session.rollback()
            return redirect(url_for("home"))
        except OperationalError as e:
            print("Erro operacional:", str(e))
            flash("Ocorreu um erro para deletar receita.", "error")
            session.rollback()
            return redirect(url_for("home"))

    else:
        flash("Ocorreu um erro para deletar receita.", "error")
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
