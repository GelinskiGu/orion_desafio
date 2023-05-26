from flask import Flask, get_flashed_messages, render_template, redirect, url_for, flash, request, abort, jsonify  # noqa: F401, E501
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin  # noqa: F401, E501
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed  # noqa: F401, E501
from datetime import datetime  # noqa: F401, E501
import os
from sqlalchemy.exc import SQLAlchemyError, InvalidRequestError, OperationalError  # noqa: F401, E501
from werkzeug.utils import secure_filename  # noqa: F401
from werkzeug.datastructures import FileStorage  # noqa: F401
from .config import SQLALCHEMY_DATABASE_URI, SECRET_KEY  # noqa: F401, E501
from .extensions import db, bcrypt
from .models import User, Category, Recipe
from .forms import LoginForm, RegisterForm, RecipeForm  # noqa: F401, E501


def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')

    basedir = os.path.abspath(os.path.dirname(__file__))
    path = './static/assets/recipes_images'

    # Configuracao banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # noqa: E501
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(
        basedir, path)

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    Session = sessionmaker(bind=engine)
    session = Session()
    db.init_app(app)  # noqa: F811

    migrate = Migrate(app, db)  # noqa: F841
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)

    @login_manager.user_loader
    def load_user(user_id):
        return session.get(User, user_id)

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
                if bcrypt.check_password_hash(user.password, form.password.data):  # noqa: E501
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
                    flash("Ocorreu um erro para o salvamento da imagem.", "error")  # noqa: E501
                    return redirect(url_for("register_new_recipe"))
                recipe = Recipe(author=current_user.id,
                                category_id=form.category.data,
                                title=form.title.data,
                                description=form.description.data,
                                ingredients=form.ingredients.data,
                                preparation_steps=form.preparation_steps.data,
                                image_filename=form.image_filename.data.filename,  # noqa: E501
                                image_path=file_url)  # noqa: E501
                try:
                    session.add(recipe)
                    session.commit()
                    flash("Receita cadastrada com sucesso!", category="success")  # noqa: E501
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
            flash("Você precisa estar logado para acessar essa página.", "error")   # noqa: E501
            return redirect(url_for('login'))
        recipes = session.query(Recipe).filter(
            Recipe.author == current_user.id).order_by(Recipe.created_at.desc()).all()  # noqa: E501

        return render_template("home.html", recipes=recipes, request=request)

    @app.route('/edit_recipe/<int:recipe_id>', methods=['GET', 'POST'])
    def edit_recipe(recipe_id):
        if not current_user.is_authenticated:
            flash("Você precisa estar logado para acessar essa página.", "error")  # noqa: E501
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
                return redirect(url_for("my_recipes"))
            except SQLAlchemyError:
                flash("Ocorreu um erro para atualizar receita.", "error")
                session.rollback()
                return redirect(url_for("home"))

        return render_template("new_recipe.html", form=form, recipe=recipe)

    @app.route('/delete_recipe/<recipe_id>')
    def delete_recipe(recipe_id):
        if not current_user.is_authenticated:
            flash("Você precisa estar logado para acessar essa página.", "error")  # noqa: E501
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
        return render_template("home.html", recipes=recipes, categories=categories)  # noqa: E501

    return app
