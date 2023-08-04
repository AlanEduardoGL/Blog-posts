from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor


# ? Creamos instancia de la clase SQLAlchemy()
db = SQLAlchemy()


# @audit def create_app
def create_app():
    # Creamos Aplicación Flask.
    app = Flask(__name__)

    # Agregamos archivo config.py
    app.config.from_object('config.Config')

    # Inicializamos la base de datos y mandamos app.
    db.init_app(app)
    
    # Configuramos CKEditor
    ckeditor = CKEditor(app)

    # Registramos las Vistas de home.py
    from blogr import home
    app.register_blueprint(home.bp)

    # Registramos las Vistas de auth.py
    from blogr import auth
    app.register_blueprint(auth.bp)

    # Registramos las Vistas de post.py
    from blogr import post
    app.register_blueprint(post.bp)

    # Importamos todo los Modulos creados.
    from .models import User, Post

    # Migramos los Modelos creados de manera automática.
    with app.app_context():
        db.create_all()

    return app
