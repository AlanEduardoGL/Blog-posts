"""
Archivo que contiene la configuración del proyecto.
"""


SQLITE = "sqlite:///project.db"
POSTGRESQL = "postgresql+psycopg2://postgres:root@localhost:5432/blogposts_db"

class Config():
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
