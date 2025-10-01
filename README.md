# Plataforma de Cursos Online

Este projeto é uma plataforma de cursos online desenvolvida com Flask, SQLAlchemy e Flask-WTF.

## Funcionalidades
- Cadastro e login de usuários
- Compra de cursos
- Área do aluno com progresso
- Área administrativa para criação e edição de cursos
- Mentorias

## Instalação

1. **Clone o repositório:**
   ```sh
   git clone <url-do-repo>
   cd myproject
   ```

2. **Crie e ative o ambiente virtual:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # ou
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados:**
   - Para desenvolvimento, o SQLite já está configurado.
   - Para criar as tabelas e aplicar migrações:
     ```sh
     flask db upgrade
     ```
   - Para popular com cursos de exemplo:
     ```sh
     python init_courses.py
     ```

5. **Execute o servidor:**
   ```sh
   flask run
   ```

6. **Acesse:**
   - http://127.0.0.1:5000/

## Requisitos
- Python 3.10+
- Flask
- Flask-WTF
- Flask-Login
- Flask-Migrate
- Flask-SQLAlchemy
- Werkzeug

## Estrutura
- `app.py`: app principal
- `models.py`: modelos do banco
- `forms.py`: formulários
- `init_db.py`: inicialização do banco
- `init_courses.py`: cursos de exemplo
- `templates/`: HTML Jinja2
- `static/`: CSS, imagens, uploads

## Observações
- Para acessar a área admin, crie um usuário e defina `is_admin=True` no banco.
- O upload de imagens de curso vai para `static/uploads/`.

---

Desenvolvido por HELEN FREIRE. 
