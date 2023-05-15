from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("home.html")


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
