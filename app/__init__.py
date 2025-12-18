from flask import Flask, render_template, request, redirect
from pathlib import Path
import os, logging
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager, login_required, current_user
from functools import wraps

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect('/login')
        if not getattr(current_user, 'is_admin', False):
            return render_template('403.html'), 403
        return fn(*args, **kwargs)
    return wrapper


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    basedir = Path(__file__).resolve().parents[2]
    env_path = os.path.join(basedir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)

    # Selección de configuración según entorno
    config_name = config_name or os.getenv('FLASK_ENV', 'production')
    if config_name == 'testing':
        db_uri = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    elif config_name == 'development':
        db_uri = os.environ.get('DEV_DATABASE_URI') or 'sqlite:///dev.db'
        app.config['DEBUG'] = True
    else:
        db_uri = os.environ.get('PROD_DATABASE_URI')
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PREFERRED_URL_SCHEME'] = 'https'

    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        secret_key = os.urandom(32)
        logging.getLogger(__name__).warning(
            'SECRET_KEY no definido. Usando clave temporal (solo desarrollo). Definir SECRET_KEY en producción.'
        )
    app.config['SECRET_KEY'] = secret_key

    is_debug = app.debug or os.getenv('FLASK_DEBUG', '0') in ('1','true','True') or os.getenv('DEBUG','0') in ('1','true','True')
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'true' if not is_debug else 'false').lower() == 'true'
    app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {'pool_pre_ping': True})

    db.init_app(app)
    migrate.init_app(app, db)

    if os.getenv('ENABLE_CSRF', 'true').lower() == 'true':
        csrf.init_app(app)
        logging.getLogger(__name__).info('CSRF protection habilitado.')
    else:
        logging.getLogger(__name__).info('CSRF protection deshabilitado.')

    # CORS restringido solo en producción
    cors_origins = os.getenv('CORS_ORIGINS')
    if config_name == 'production':
        if cors_origins:
            origins_list = [o.strip() for o in cors_origins.split(',') if o.strip()]
            CORS(app, resources={r"/*": {"origins": origins_list}})
            logging.getLogger(__name__).info(f'CORS restringido a: {origins_list}')
        else:
            CORS(app, resources={r"/*": {"origins": []}})
            logging.getLogger(__name__).warning('CORS bloqueado (no hay CORS_ORIGINS definido)')
    else:
        CORS(app)
        logging.getLogger(__name__).warning('CORS abierto (no producción).')

    from app.resources.club_resource import clubs_bp
    from app.resources.jugadora_resource import jugadora_bp
    from app.resources.resultado_resource import resultado_bp
    from app.resources.usuario_resource import usuario_bp
    from app.resources.equipo_resource import equipo_bp
    from app.resources.categorias_resource import categorias_bp
    from app.resources.posiciones_resource import posiciones_bp
    from app.resources.torneo_resource import torneo_bp
    from app.resources.noticia_resource import noticia_bp
    from app.resources.partido_resource import partido_bp
    from app.resources.incidencia_resource import incidencia_bp
    from app.resources.cuerpo_tecnico_resource import bp_cuerpo_tecnico
    from app.resources.arbitro_resource import arbitro_bp
    from app.resources.resultados_resource import resultados_bp
    from app.repositories.usuario_repositorio import UsuarioRepositorio
    from app.models.usuario import Usuario
    from app.routes_static import static_bp

    login_manager.init_app(app)
    login_manager.login_view = 'login_page'

    @login_manager.user_loader
    def load_user(user_id):
        return UsuarioRepositorio.buscar_por_id(user_id)

    app.register_blueprint(clubs_bp)
    app.register_blueprint(jugadora_bp)
    app.register_blueprint(resultado_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(equipo_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(posiciones_bp)
    app.register_blueprint(torneo_bp)
    app.register_blueprint(noticia_bp)
    app.register_blueprint(partido_bp)
    app.register_blueprint(incidencia_bp)
    app.register_blueprint(bp_cuerpo_tecnico)
    app.register_blueprint(arbitro_bp)
    app.register_blueprint(resultados_bp)
    app.register_blueprint(static_bp)

    # ...rutas estáticas eliminadas, ahora en routes_static.py...

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

    app.view_functions['static_pages.carga_incidencias'] = require_permission('puede_cargar_incidencias')(app.view_functions['static_pages.carga_incidencias'])
    app.view_functions['static_pages.precarga_equipos'] = require_permission('puede_precargar_equipos')(app.view_functions['static_pages.precarga_equipos'])

    @app.after_request
    def set_security_headers(resp):
        resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
        resp.headers.setdefault('X-Frame-Options', 'DENY')
        resp.headers.setdefault('Referrer-Policy', 'no-referrer-when-downgrade')
        # Content Security Policy para prevenir XSS
        # Permitir imágenes desde Cloudinary, estilos de Cloudflare y frames de Google
        resp.headers.setdefault('Content-Security-Policy',
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://www.instagram.com; "
            "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https://res.cloudinary.com; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-src https://www.google.com https://www.facebook.com https://www.instagram.com; "
            "frame-ancestors 'none'; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        try:
            if request.is_secure or app.config.get('SESSION_COOKIE_SECURE'):
                resp.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
        except Exception:
            pass

        # Cache agresivo solo para archivos estáticos
        try:
            if request.path.startswith('/static/'):
                # 30 días
                resp.headers.setdefault('Cache-Control', 'public, max-age=2592000, immutable')
        except Exception:
            pass
        try:
            if 'csrf' in app.extensions:
                token = generate_csrf()
                resp.set_cookie(
                    'XSRF-TOKEN',
                    token,
                    secure=app.config.get('SESSION_COOKIE_SECURE', True),
                    httponly=False,
                    samesite=app.config.get('SESSION_COOKIE_SAMESITE', 'Lax'),
                )
        except Exception as e:
            logging.getLogger(__name__).debug(f'No se pudo generar cookie CSRF: {e}')
        return resp

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    @app.before_request
    def enforce_https():
        force_https = os.getenv('FORCE_HTTPS', 'true').lower() == 'true'
        if not force_https or app.debug:
            return
        if request.is_secure:
            return
        xf_proto = request.headers.get('X-Forwarded-Proto', '')
        if 'https' in xf_proto:
            return
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)


    # ADVERTENCIA: Usa un usuario de base de datos con privilegios mínimos en producción.
    # Ejemplo: solo permisos de SELECT/INSERT/UPDATE/DELETE según necesidad, nunca superusuario.
    # Las credenciales deben estar solo en variables de entorno y nunca en el código fuente.
    return app


app = create_app()

__all__ = ["create_app", "app", "db", "login_manager", "csrf", "require_admin"]
