from flask import Blueprint

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return "Página de inicio."


@bp.route('/blog')
def blog():
    return "Página de blog."