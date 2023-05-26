from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField  # noqa: F401, E501
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo  # noqa: F401, E501

from extensions import bcrypt

from models import User

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
