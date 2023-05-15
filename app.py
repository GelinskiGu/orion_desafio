from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:8rPTT7k#gT@localhost/orion_desafio.db'  # noqa: E501
db.init_app(app)


@app.route("/")
def hello_world():
    return render_template("base.html")


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
