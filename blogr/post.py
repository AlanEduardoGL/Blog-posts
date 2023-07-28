from flask import Blueprint

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/posts')
def posts():
    return "Página de posts"


@bp.route('/create')
def create():
    return "Página de create"


@bp.route('/update')
def update():
    return "Página de update"