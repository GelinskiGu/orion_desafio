from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin  # noqa: F401, E501
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo  # noqa: F401, E501
from flask_wtf import FlaskForm

# Configuracao banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8rPTT7k#gT@localhost/orion'  # noqa: E501
app.config['SECRET_KEY'] = 'qTUL^P3cQ%'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


@app.route("/")
def hello_world():
    return render_template("base.html")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,
                        password=hashed_password, name=form.name.data)  # noqa: E501
        print("Usuário criado.")
        db.session.add(new_user)
        db.session.commit()
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
                return "Usuário logado."

    return render_template("login.html", form=form)


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
