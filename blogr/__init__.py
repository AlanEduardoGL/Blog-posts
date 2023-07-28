from flask import Flask

def create_app():
    # ? Creamos Aplicación Flask
    app = Flask(__name__)

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