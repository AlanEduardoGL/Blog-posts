import functools
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from .models import User
from blogr import db
# Elimina espacios de una imagen y agrega barra baja.
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError


# Creamos Blueprint /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')


# @audit Route /register
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Ruta/vista que registra un nuevo usuario.
    Recibe methods 'GET' y 'POST'.

    Returns:
        redirect: (auth.login) Nos redirige al login.
        error: Se mostrará un mensaje de error si existe el usuario.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Registramos el usuario.
        user = User(username, email, generate_password_hash(password))

        # Validamos que correo no existan en la base de datos.
        user_email = User.query.filter_by(email=email).first()

        error = None

        if user_email is None:
            try:
                db.session.add(user)
                db.session.commit()

            except SQLAlchemyError as e:
                error = f'Error interno al registrar el usuario "{username}". Mensaje: {str(e)}.'

            else:
                return redirect(url_for('auth.login'))

        else:
            error = f"El correo {email} ya se encuentra registrado."

        flash(error)

    return render_template('auth/register.html')


# @audit Route /login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Ruta/vista para iniciar sesión del usuario.
    Recibe methods 'GET' y 'POST'.

    Returns:
        redirect: (post.posts) Nos redirige a nuestros posts publicados.
        error: Se mostrará un mensaje de error si no coinciden las credenciales.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        error = None

        if user is None or not check_password_hash(user.password, password):
            error = "El correo y/o contraseña ingresados son incorrectos."
        else:
            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('post.posts'))

        flash(error)

    return render_template('auth/login.html')


# @audit Function load_logged_in_user()
@bp.before_app_request
def load_logged_in_user():
    """ 
    Mantiene la session del usuario activa.
    Se ejecuta antes de cada solicitud entrante a la aplicación 
    (antes de que se maneje una vista).

    Returns:
        g.user: Alamcena todos los datos del usuario 
        activo en la session.
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        try:
            g.user = User.query.get(user_id)

        except SQLAlchemyError as e:
            print(
                f'No existe usuario registrado con id "{user_id}". Mensaje: {str(e)}.')


# @audit Route /logout
@bp.route('/logout')
def logout():
    """
    Ruta/vista para cerrar session del usuario.

    Returns:
        redirect: Nos redirije al index principal.
    """
    try:
        session.clear()

    except SQLAlchemyError as e:
        print(
            f'Error interno al cerrar sesión. Intenta nuevamente. Mensaje: {str(e)}')

    else:
        return redirect(url_for('home.index'))


# @audit Function login_required()
def login_required(view):
    """
    Asegura que el usuario haya iniciado session
    antes de que pueda acceder a una vista o ruta específica.

    Args:
        view (vista): La vista representa la función que se asocia con 
        una ruta específica en la aplicación.

    Returns:
        redirect: (auth.login) Si el usuario no ha iniciado sesión, 
        se redirige automáticamente a la página de inicio.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)

    return wrapped_view


# @audit Route /profile
@bp.route('/profile/<int:id>', methods=['GET', 'POST'])
@login_required  # Está vista requiere session activa.
def profile(id):
    """
    Ruta/vista que edita el perfil del usuario.
    Recibe methods 'GET' y 'POST'.

    Args:
        id (int): Recibe el id del usuario para obtener todos los datos.

    Returns:
        redirect: Redirige a (auth.profile) si los cambios fueron correctos.
        error: Mensaje de error si la contraseña no cumple
        con lo requerido.
    """
    user = User.query.get(id)

    if not user:
        flash("Usuario no encontrado.")

        return redirect((url_for('home.index')))

    if request.method == "POST":
        user.username = request.form.get('username')
        password = request.form.get('password')

        error = None

        if password:
            user.password = generate_password_hash(password)
        elif len(password) > 0 and len(password) < 6:
            error = "La contraseña debe tener más de 5 caracteres."

        if request.files['photo']:
            try:
                # Obtenemos la imagen del formulario.
                photo = request.files['photo']
                # Como se va a guardar la imagen.
                photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')
                # Guardamos en el campo "photo" la imagen en la Base de Datos.
                user.photo = f'media/{secure_filename(photo.filename)}'
                
            except SQLAlchemyError as e:
                error = f'Error al guardar nueva foto de perfíl. Intenta nuevamente. Mensaje: {str(e)}.'

        if error is not None:
            flash(error)
        else:
            try:
                db.session.commit()

            except Exception as e:
                db.session.rollback()
                error = f"Error al guardar los cambios en la base de datos, inténtalo de nuevo más tarde. Código de error: {str(e)}"

            else:
                return redirect(url_for('auth.profile', id=user.id))

        flash(error)

    return render_template('auth/profile.html', user=user)
