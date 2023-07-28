from flask import Blueprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register')
def register():
    return "Página de registro."


@bp.route('/login')
def login():
    return "Página de login."


@bp.route('/profile')
def profile():
    return "Página de profile"