from flask import (
    Blueprint, 
    render_template, 
    request
)
from .models import (
    User, 
    Post
)
from sqlalchemy.exc import SQLAlchemyError


# Creamos Blueprint home
bp = Blueprint('home', __name__)


def get_user(id):
    """
    Function para obtener datos el usuario.

    Args:
        id (int): Se espera recibir el id del usuario 
        a obtener en la consulta.

    Returns:
        user: Retorna todo los datos del usuario.
    """
    try:
        user = User.query.get(id)
    
    except SQLAlchemyError as e:
        print(f'No se encontro usuairo on id "{id}". Mensaje: {str(e)}.')
    
    else:
        return user
    
    
def search_post(query):
    """
    Function que búsca los blogs públicados
    por el usuario, Por título.

    Args:
        query (string): Se espera el texto escrito
        por el usuario en la búsqueda.

    Returns:
        posts: Retorna el resultado de búsqueda.
        Blog públicado.
    """
    try:
        posts = Post.query.filter(Post.title.ilike(f'%{query}%')).all()
    except SQLAlchemyError as e:
        print(f'Error al búscar el Blog "{query}. Mensaje: {str(e)}"')
    else:
        return posts
    

# @audit Route /
@bp.route('/', methods=['GET', 'POST'])
def index():
    """
    Function que muestra la página principal
    de la página principal. Y obtiene todos los
    posts públicados por el usuario.

    Returns:
        render_template: Renderiza la plantilla index.html
    """
    try:
        posts = Post.query.all()
        
        if request.method == 'POST':
            query = request.form.get('search')
            posts = search_post(query)
            value = "hidden"
            
            return render_template('index.html', posts=posts, get_user=get_user, value=value)
        
    except SQLAlchemyError as e:
        print(f'Error al traer Blogs públicados. Mensaje: {str(e)}')
        
    return render_template('index.html', posts=posts, get_user=get_user)


# @audit Route /blog
@bp.route('/blog/<url>')
def blog(url):
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        post = Post.query.filter_by(url=url).first()
    except SQLAlchemyError as e:
        print(f'Error al búscar url "{url}" en la base de datos. Mensaje: {str(e)}.')
    
    return render_template('blog.html', post=post, get_user=get_user)