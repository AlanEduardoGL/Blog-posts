from blogr import db
from datetime import datetime


# ? @audit Tabla Users
class User(db.Model):
    # ? Colocamos nombre tabla.
    __tablename__ = "users"

    # ? Colocamos columnas tabla.
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(200))

    # ? Creamos el Metodo Constructor.
    def __init__(self, username, email, password, photo=None):
        self.username = username
        self.email = email
        self.password = password
        self.photo = photo

    # ? Colocamos como vamos a representar cada uno de estos elementos en el Shell.
    def __repr__(self):
        return f"User: {self.username}"


# ? @audit Tabla Posts
class Post(db.Model):
    # ? Colocamos nombre tabla.
    __tablename__ = "posts"

    # ? Colocamos columnas tablas.
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    info = db.Column(db.Text)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # ? Creamos el Metodo Constructor
    def __init__(self, author, url, title, info, content) -> None:
        self.author = author
        self.url = url
        self.title = title
        self.info = info
        self.content = content

    # ? Colocamos como vamos a representar cada uno de estos elementos en el Shell.
    def __repr__(self) -> str:
        return f"Post: {self.title}"