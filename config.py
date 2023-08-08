"""
Archivo que contiene la configuración del proyecto.
"""


SQLITE = "sqlite:///project.db"
# ! Cambiar el Port si es Windows o Macbook !
# ! Windows Port: 5432 "Versión PostgreSQL 15" !
# ! Macbook Port: 5433 "Versión PostgreSQL 11" ! 
POSTGRESQL = "postgresql+psycopg2://postgres:root@localhost:5433/blogposts_db"


# @audit Class Config
class Config():
    DEBUG = True
    SECRET_KEY = 'dev'
    SQLALCHEMY_DATABASE_URI = POSTGRESQL
    # * Configuramos CKEditor
    """
    basic
    standard （default value）
    full
    standard-all (only available from CDN)
    full-all (only available from CDN)
    """
    CKEDITOR_PKG_TYPE = 'full'
