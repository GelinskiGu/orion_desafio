<h1> Receitas Orion </h1>


![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

* [Acesso ao Projeto](#acesso-ao-projeto)

# 📁 Acesso ao projeto
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
<p>
  Após executar essas etapas, apenas falta instalar o Tailwind, framework do CSS utilizado para fazer o frontend do projeto. Para fazer isso, basta executar:
</p>

  ```
  npx tailwindcss -i static/assets/css/style.css -o static/css/output.css
  ```

<p>
  Agora está tudo configurado! Para iniciar o servidor Flask:
</p>

   ```
  py app.py
  ```

  Acesse o projeto no navegador usando a URL __http://localhost:5000__  , em que, por padrão, localhost é **http://127.0.0.1**

