from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    # ? Creamos Aplicación Flask
    app = Flask(__name__)

    # ? Agregamos archivo config.py
    app.config.from_object('config.Config')

    # ? Inicializamos la base de datos
    db.init_app(app)

    # ? Registramos las Vistas de home.py
    from blogr import home 
    app.register_blueprint(home.bp)

    # ? Registramos las Vistas de auth.py
    from blogr import auth
    app.register_blueprint(auth.bp)

    # ? Registramos las Vistas de post.py
    from blogr import post
    app.register_blueprint(post.bp)

    return app