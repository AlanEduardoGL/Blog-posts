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


# @audit Route /create
@bp.route('/create', methods=['GET', 'POST'])
@login_required  # ! Decorador para requerir la session en esta vista.
def create():
    """
    Ruta/vista para crear un nuevo post.

    Returns:
        redirect: Redirige a (post.posts) si fue exitoso el registro.
        flash(error): Mostrara mensaje de error en caso de existir el registro.
    """
    if request.method == 'POST':
        url = request.form.get('url')
        # Remplazamos espacios con guinoes.
        url = url.replace(' ', '-')
        title = request.form.get('title')
        info = request.form.get('info')
        # Llamamos "ckeditor" para obtener content
        content = request.form.get('ckeditor')

        # Creamos nuevo post.
        post = Post(g.user, url, title, info, content)

        error = None

        # Comprobamos url de post con los existentes.
        post_url = Post.query.filter_by(url=url).first()

        if post_url == None:
            # Guardamos en la base de datos y confirmamos cambios.
            db.session.add(post)
            db.session.commit()
            flash(f'El blog {post.title} se agrego correctamente.')

            return redirect(url_for('post.posts'))
        else:
            error = f'La URL "{url}" ya existe. Intenta nuevamente.'

    flash(error)

    return render_template('admin/create.html')


# @audit Route /update
@bp.route('/update')
@login_required  # ! Decorador para requerir la session en esta vista.
def update():
    return render_template('admin/update.html')
