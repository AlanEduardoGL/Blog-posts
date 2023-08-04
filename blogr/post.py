from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    flash,
    url_for,
    g
)
from .auth import login_required
from .models import Post
from blogr import db
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    validators
)


# Creamos Blueprint /post
bp = Blueprint('post', __name__, url_prefix='/post')


# @audit Route /posts
@bp.route('/posts')
@login_required  # ! Decorador para requerir la session en esta vista.
def posts():
    posts = Post.query.all()

    return render_template('admin/posts.html', posts=posts)


# @audit Class MyForm
class MyForm(FlaskForm):
    name = StringField("Nombre Post", validators=[validators.DataRequired()])


# @audit Route /create
@bp.route('/create')
@login_required  # ! Decorador para requerir la session en esta vista.
def create():
    # Instanciamos la Class MyForm
    form = MyForm()

    return render_template('admin/create.html')


# @audit Route /update
@bp.route('/update')
@login_required  # ! Decorador para requerir la session en esta vista.
def update():
    return render_template('admin/update.html')
