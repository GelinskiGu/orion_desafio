<h1> Blog de Receitas </h1>


![Badge em Desenvolvimento](http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=GREEN&style=for-the-badge)

* [Descrição](#descricao)
* [Tecnologias utilizadas](#tecnologias-utilizadas)
* [Acesso ao Projeto](#acesso-ao-projeto)
* [Próximas Implementações](#proximas-implementacoes)

## Descrição <a name="descricao"></a>
<p>Este projeto é uma plataforma para compartilhamento de receitas culinárias. Os usuários podem criar, editar, compartilhar e excluir suas receitas com outros usuários da plataforma.</p> 
<p>Cada receita possui um título, uma categoria, uma descrição, uma lista de ingredientes, um conjunto de instruções passo-a-passo para prepará-la e uma imagem.</p>
Na página inicial as receitas são ordenadas por data de criação, sendo as primeiras as últimas a terem sido criadas. Porém, é possível filtrar as receitas por categoria.

##  Tecnologias utilizadas <a name="tecnologias-utilizadas"></a>
- Python
- Flask
- Tailwind CSS
- Javascript
- PostgreSQL

## 📁 Acesso ao projeto <a name="acesso-ao-projeto"></a>
O deploy do repositório está disponível em: **[https://www.recipes-blog.gelinski.dev/](https://www.recipes-blog.gelinski.dev/)**.

### Executando localmente

#### Pré-requisitos

- Python
- pip

#### Configuração

1. Clone o repositório:

   ```bash
   git clone https://github.com/GelinskiGu/recipe_blog.git

2. Navegue até o diretório do projeto:

    ```bash
    cd orion_desafio
    ```
    
3. Crie e ative um ambiente virtual:
     
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Para Linux/Mac
    .venv\Scripts\activate.bat  # Para Windows
    ```
    
4. Instale as dependências do Python e do Flask:

    ```bash
    pip install -r requirements.txt
    ```
    
5. Configure o banco de dados:

   - No diretório `myapp/`, crie um arquivo `config.py` e adicione o seguinte código:

     ```python
     SQLALCHEMY_DATABASE_URI = "<Endereço do banco de dados>"
     SECRET_KEY = "<Chave secreta>"
     ```

   - No arquivo `__init__.py`, comente as linhas:

     ```python
     # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
     # app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
     ```

     e descomente as linhas:

     ```python
     from .config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
     app.config['SECRET_KEY'] = SECRET_KEY
     ```
     
6. Execute o servidor Flask:
    
    ```bash
    py run.py
    ```
7. Acesse o projeto no navegador utilizando a URL __http://localhost:5000__.

## Próximas Implementações <a name="proximas-implementacoes"></a>
Aqui estão algumas melhorias planejadas para o projeto:

- Implementar um servidor na nuvem ligado ao deploy da aplicação, para armazenar as imagens das receitas salvas ou editadas.
- Mudar o banco de dados para adicionar a funcionalidade de adicionar receitas favoritas/salvas.
- Implementar uma barra de pesquisa de receitas para facilitar a busca por títulos ou ingredientes.
