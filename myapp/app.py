from flask import Flask, get_flashed_messages, render_template, redirect, url_for, flash, request, abort, jsonify  # noqa: F401, E501
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin  # noqa: F401, E501
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class, UploadNotAllowed  # noqa: F401, E501
from datetime import datetime  # noqa: F401, E501
import os
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError, OperationalError  # noqa: F401, E501
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY  # noqa: F401, E501
from extensions import db, bcrypt
from models import User, Category, Recipe
from forms import LoginForm, RegisterForm, RecipeForm  # noqa: F401, E501

basedir = os.path.abspath(os.path.dirname(__file__))
path = './static/assets/recipes_images'

# Configuracao banco de dados
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # noqa: E501
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(
    basedir, path)

# bcrypt = Bcrypt(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

Session = sessionmaker(bind=engine)
session = Session()
db.init_app(app)  # noqa: F811

migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

"""
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


@login_manager.user_loader
def load_user(user_id):
    return session.get(User, user_id)


"""
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
            min=5, max=20)],
        render_kw={"placeholder": "Seu nome de usuário"})
    password = PasswordField(label="Senha",
                             validators=[InputRequired(),
                                         Length(min=8, max=20)],
                             render_kw={"placeholder": "Sua senha"})
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
    title = TextAreaField(label="Título da receita", validators=[InputRequired(), Length(max=255)],  # noqa: E501
                          render_kw={"placeholder": "Título de sua receita"})
    category = SelectField('Categoria', coerce=int)
    description = TextAreaField(label="Descrição da receita", validators=[InputRequired()],  # noqa: E501
                                render_kw={"placeholder": "Descrição de sua receita"})  # noqa: E501
    ingredients = TextAreaField(label="Ingredientes da receita", validators=[InputRequired()],  # noqa: E501
                                render_kw={"placeholder": "Insira um ingrediente por linha"})  # noqa: E501
    preparation_steps = TextAreaField(label="Passos de preparo da receita", validators=[InputRequired()],  # noqa: E501
                                      render_kw={"placeholder": "Insira um passo por linha"})  # noqa: E501
    image_filename = FileField("Imagem da receita",
                               validators=[InputRequired()],
                               description="Coloque sua imagem da receita")
    submit = SubmitField('Cadastrar')


session.delete_all()

categories = [
    Category(name='Entradas'),
    Category(name='Lanches'),
    Category(name='Pratos Principais'),
    Category(name='Bebidas'),
    Category(name='Sobremesas'),
    Category(name='Outros'),
]
session.add_all(categories)
session.commit()

 """


@app.route("/")
def home():
    # TODO: try except
    recipes = session.query(Recipe).order_by(
        Recipe.created_at.desc()).all()
    categories = session.query(Category).all()
    context = {
        'recipes': recipes,
        'categories': categories
    }
    print(recipes)
    print(categories)
    return render_template("home.html", **context)  # noqa: E501
  # noqa: E501


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
    if current_user.is_authenticated:
        flash('Você já está logado.', 'error')
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))

    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


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
                            image_path=file_url)  # noqa: E501
            try:
                session.add(recipe)
                session.commit()
                flash("Receita cadastrada com sucesso!", category="success")
                return redirect(url_for("home"))
            except SQLAlchemyError:
                flash("Ocorreu um erro para cadastrar receita.", "error")
                session.rollback()
                return redirect(url_for("register_new_recipe"))

    else:
        # Usuário não logado
        flash("Você precisa estar logado para acessar essa página.",
              category="error")
        return redirect(url_for('login'))

    return render_template("new_recipe.html", form=form, recipe=None)


@app.route('/my_recipes')
def my_recipes():
    if not current_user.is_authenticated:
        flash("Você precisa estar logado para acessar essa página.", "error")
        return redirect(url_for('login'))
    recipes = session.query(Recipe).filter(
        Recipe.author == current_user.id).order_by(Recipe.created_at.desc()).all()  # noqa: E501

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

    form = RecipeForm()

    categories = session.query(Category).order_by(
        Category.name.asc()).all()

    # TODO: Transformar em um set para deixar
    # como primeira a categoria selecionada.
    form.category.choices = [(category.id, category.name)
                             for category in categories]
    if form.validate_on_submit():
        now = datetime.now()
        path_image = f"{now.year}/{now.strftime('%m')}"
        try:
            image_file = request.files['image_filename']
            filename = photos.save(
                image_file, folder=path_image)
            file_url = photos.url(filename)
        except UploadNotAllowed:
            flash("Ocorreu um erro para o salvamento da imagem.", "error")
            return redirect(url_for("home"))
        recipe.title = form.title.data
        recipe.category_id = form.category.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.preparation_steps = form.preparation_steps.data
        recipe.image_filename = form.image_filename.data.filename
        recipe.image_path = file_url

        try:
            session.commit()
            flash("Receita atualizada com sucesso!", "success")
            return redirect(url_for("home"))
        except SQLAlchemyError:
            flash("Ocorreu um erro para atualizar receita.", "error")
            session.rollback()
            return redirect(url_for("home"))

    return render_template("new_recipe.html", form=form, recipe=recipe)


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


@app.route('/recipe_details/<recipe_id>')
def recipe_details(recipe_id):
    recipe = session.get(Recipe, recipe_id)
    if recipe is None:
        abort(404)
    author = session.query(User).get(recipe.author)
    steps = recipe.preparation_steps.split('\n')
    ingredients = recipe.ingredients.split('\n')
    return render_template("recipe_details.html", recipe=recipe, author=author, steps=steps, ingredients=ingredients)  # noqa: E501


@app.route('/category/<category_id>')
def category(category_id):
    recipes = session.query(Recipe).filter(Recipe.category_id == category_id).order_by(Recipe.created_at.desc()).all()  # noqa: E501
    categories = session.query(Category).all()
    if category is None:
        abort(404)
    return render_template("home.html", recipes=recipes, categories=categories)


if __name__ == '__main__':
    app.run(debug=True)
