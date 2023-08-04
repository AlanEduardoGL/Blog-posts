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
from sqlalchemy.exc import SQLAlchemyError


# Creamos Blueprint /post
bp = Blueprint('post', __name__, url_prefix='/post')


# @audit Route /posts
@bp.route('/posts')
@login_required  # ! Decorador para requerir la session en esta vista.
def posts():
    """
    Ruta/vista que muestra todos los posts publicados por el usuario.

    Returns:
        render_template: Muestra la plantilla (admin/posts.html).
    """
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

        # Creamos nuevo post incluyendo el id del usuario.
        post = Post(g.user.id, url, title, info, content)

        error = None

        # Comprobamos url de post con los existentes.
        post_url = Post.query.filter_by(url=url).first()

        if post_url == None:
            try:
                # Guardamos en la base de datos y confirmamos cambios.
                db.session.add(post)
                db.session.commit()
                flash(f'El blog "{post.title}" se agrego correctamente.')

                return redirect(url_for('post.posts'))
            
            except SQLAlchemyError as e:
                # Deshacer cambios en caso de error
                db.session.rollback()
                error = f'Error al guardar el post: {str(e)}'
                flash(error)

        else:
            error = f'La URL "{url}" ya existe. Intenta nuevamente.'

        flash(error)

    return render_template('admin/create.html')


# @audit Route /update
@bp.route('/update')
@login_required  # ! Decorador para requerir la session en esta vista.
def update():
    return render_template('admin/update.html')
