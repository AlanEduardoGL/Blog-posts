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
@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required  # ! Decorador para requerir la session en esta vista.
def update(id):
    """
    Routa/vista que actualiza un post publicado
    por el usuario.

    Args:
        id (int): id del post a editar

    Returns:
        redirect: Nos redirige a los posts del usuario
        en caso de exito.
        render_template: Nos redirige a udate.html en caso de error.
    """
    try:
        # Obtenemos todo los datos del post públicado.
        post = Post.query.get_or_404(id)

    except SQLAlchemyError as e:
        # Deshacer cambios en caso de error
        db.session.rollback()
        flash(
            f'No existe post públicado con el id {id}: Código error => {str(e)}')

    if request.method == 'POST':
        post.title = request.form.get('title')
        post.info = request.form.get('info')
        post.content = request.form.get('content')

        try:
            # Confirmamos los cambios a la base de datos.
            db.session.commit()

        except SQLAlchemyError as e:
            # Deshacer cambios en caso de error
            db.session.rollback()
            flash(f'Ha ocurrido un error al actualizar el blog {post.title}. Inténtalo de nuevo. Código error => {str(e)}')

        else:
            flash(f'El blog {post.title} se actualizo correctamente.')

            return redirect(url_for('post.posts'))

    return render_template('admin/update.html', post=post)


# @audit Route /delete
@bp.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required  # ! Decorador para requerir la session en esta vista.
def delete(id):
    """
    Ruta/vista que elimina el post seleccionado por el usuario.

    Args:
        id (int): id del post a eliminar.

    Returns:
        redirect: Nos redirige a los post públicados
        por el usuario si fue o no eliminado el post.
        Con mensaje error o success.
    """
    try:
        # Obtenemos todo los datos del post públicado.
        post = Post.query.get_or_404(id)

        # Eliminamos el post.
        db.session.delete(id)
        # Confirmamos los cambios en al base de datos.
        db.session.commit()

        flash(f'Se elimino con exito el blog "{post.title}".')

        return redirect(url_for('post.posts'))

    except SQLAlchemyError as e:
        # Deshacer cambios en caso de error
        db.session.rollback()
        
        flash(f'Error al eliminar blog "{post.title}". Código error => {str(e)}')

        return redirect(url_for('post.posts'))