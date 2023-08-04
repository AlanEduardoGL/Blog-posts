from flask import Blueprint, render_template


# Creamos Blueprint home
bp = Blueprint('home', __name__)


# @audit Route /
@bp.route('/')
def index():
    return render_template('index.html')


# @audit Route /blog
@bp.route('/blog')
def blog():
    return render_template('blog.html')