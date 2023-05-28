<h1> Receitas Orion </h1>


![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

* [Acesso ao Projeto](#acesso-ao-projeto)

# 📁 Acesso ao projeto
O deploy do repositório está disponível em: **https://www.recipes-blog.gelinski.dev/**.

Caso queira rodar localmente:

<p>
  Inicialmente precisa ter o Python instalado.
  Após isso, é necessário a criação de um ambiente virtual. No diretório onde você clonou o projeto do github executar o seguinte comando:
</p>

  ```
  python -m venv .venv
  ```
<p>
  Isso irá criar uma pasta .venv/ em seu diretório. Para ativar o ambiente virtual:
</p>

  ```
  ./.venv/Scripts/activate.bat
  ```
<p>
  Agora, é necessário instalar as dependências do Python e do Flask para rodar a aplicação. No diretório há um "requirements.txt" onde está listado todos os pacotes e suas versões utilizadas no projeto.
  Para instalar automaticamente, basta rodar o comando:
</p>

  ```
  pip install -r requirements.txt
  ```
  
  Para fazer a configuração do banco de dados, no diretório myapp/ é necessário criar um arquivo **config.py**. Nesse arquivo é necessário o seguinte código:

  ```
  SQLALCHEMY_DATABASE_URI = <Endereço de seu banco de dados>
  SECRET_KEY = <Qualquer chave secreta>
  ```

  No arquivo __init__.py basta comentar e descomentar as seguintes linhas:

  ```
    from .config import SQLALCHEMY_DATABASE_URI, SECRET_KEY 

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = SECRET_KEY
  # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
  # app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
  ```
No arquivo run.py, no diretório principal basta incluir a seguinte linha de código no final do arquivo:
 
  ```
  app.run(debug=True)
  ```

<p>
  Agora está tudo configurado! Para iniciar o servidor Flask:
</p>

   ```
  py run.py
  ```

  Acesse o projeto no navegador usando a URL __http://localhost:5000__  , em que, por padrão, localhost é **127.0.0.1**.

