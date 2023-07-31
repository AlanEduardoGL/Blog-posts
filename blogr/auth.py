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

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Function que registra un nuevo usuario.

    Returns:
        redirect: (auth.login) Nos redirige al login.
        error: Se mostrará un mensaje de error si existe el usuario.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # ? Registramos el usuario.
        user = User(username, email, generate_password_hash(password))

        # ? Validamos que correo no existan en la base de datos.
        user_email = User.query.filter_by(email=email).first()

        error = None

        if user_email == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f"El correo {email} ya se encuentra registrado."

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function para iniciar session.

    Returns:
        redirect: (post.posts) Nos redirige a nuestros posts publicados.
        error: Se mostrará un mensaje de error si no coinciden las credenciales.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        error = None

        if user == None or not check_password_hash(user.password, password):
            error = "El correo y/o contraseña ingresados son incorrectos."
        else:
            if error is None:
                session.clear()
                session['user_id'] = user.id
                return redirect(url_for('post.posts'))

        flash(error)

    return render_template('auth/login.html')


# ? Decorador para mantener/guardar la session.
@bp.before_app_request
def load_logged_in_user():
    """ 
    Mantiene la session del usuario activa.
    Se ejecuta antes de cada solicitud entrante a la aplicación 
    (antes de que se maneje una vista).

    Returns:
        g.user: Obtenemos id del usuario de la session utilizada y es almacenado en (g.user).
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route('/logout')
def logout():
    """
    Function para cerrar session.

    Returns:
        redirect: Nos redirije al index principal.
    """
    session.clear()
    return redirect(url_for('home.index'))


# ? Decorador para requerir la session.
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


@bp.route('/profile')
def profile():
    return "Página de profile"
