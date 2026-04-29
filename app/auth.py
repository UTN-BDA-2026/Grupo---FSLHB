"""Autenticación y decoradores de permisos."""

from functools import wraps

from flask import redirect, render_template
from flask_login import current_user


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        if not getattr(current_user, 'is_admin', False):
            return render_template('403.html'), 403
        return fn(*args, **kwargs)

    return wrapper


def require_permission(attr_name: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect('/login')
            if not getattr(current_user, attr_name, False):
                return render_template('403.html'), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def init_login(app) -> None:
    # Imports diferidos para evitar ciclos (Usuario -> db -> app)
    from app.extensions import login_manager
    from app.repositories.usuario_repositorio import UsuarioRepositorio

    login_manager.init_app(app)
    login_manager.login_view = 'login_page'

    @login_manager.user_loader
    def load_user(user_id):
        return UsuarioRepositorio.buscar_por_id(user_id)


def apply_static_page_permissions(app) -> None:
    """Aplica wrappers de permisos a endpoints estáticos (si existen)."""

    view_functions = getattr(app, 'view_functions', {})

    carga = view_functions.get('static_pages.carga_incidencias')
    if carga is not None:
        view_functions['static_pages.carga_incidencias'] = require_permission(
            'puede_cargar_incidencias'
        )(carga)

    precarga = view_functions.get('static_pages.precarga_equipos')
    if precarga is not None:
        view_functions['static_pages.precarga_equipos'] = require_permission(
            'puede_precargar_equipos'
        )(precarga)
