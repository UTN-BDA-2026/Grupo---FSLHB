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


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    basedir = Path(__file__).resolve().parents[2]
    env_path = os.path.join(basedir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)

    # testing usa sqlite en memoria
    if config_name == 'testing':
        db_uri = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        db_uri = (
            os.environ.get('DATABASE_URL')
            or os.environ.get('PROD_DATABASE_URI')
            or os.environ.get('DEV_DATABASE_URI')
            or 'postgresql://hockeyuser:hockeypass@localhost:5433/hockey'
        )
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

    cors_origins = os.getenv('CORS_ORIGINS')
    if cors_origins:
        origins_list = [o.strip() for o in cors_origins.split(',') if o.strip()]
        CORS(app, resources={r"/*": {"origins": origins_list}})
        logging.getLogger(__name__).info(f'CORS restringido a: {origins_list}')
    else:
        CORS(app)
        logging.getLogger(__name__).warning('CORS abierto. Definir CORS_ORIGINS para restringir en producción.')

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

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/autoridades')
    def autoridades():
        return render_template('autoridades.html')

    @app.route('/reglamento')
    def reglamento():
        return render_template('reglamento.html')

    @app.route('/historial')
    def historial():
        return render_template('historial.html')

    @app.route('/contacto')
    def contacto():
        return render_template('contacto.html')

    @app.route('/galeria')
    def galeria():
        return render_template('galeria.html')

    @app.route('/club-panel')
    def club_panel():
        return render_template('club-panel.html')

    @app.route('/panel-clubes')
    @login_required
    def panel_clubes():
        return render_template('panel-clubes.html')

    @app.route('/noticias')
    def noticias():
        return render_template('noticias.html')

    @app.route('/calendario')
    def calendario():
        return render_template('calendario.html')

    @app.route('/clubes')
    def clubes():
        return render_template('clubes.html')

    @app.route('/equipos')
    def equipos():
        return render_template('equipos.html')

    @app.route('/sponsors')
    def sponsors():
        return render_template('sponsors.html')

    @app.route('/login')
    def login_page():
        return render_template('login.html')

    @app.route('/precarga-equipos')
    @login_required
    def precarga_equipos():
        return render_template('precarga-equipos.html')

    @app.route('/crear-lista-buena-fe')
    @login_required
    def crear_lista_buena_fe():
        return render_template('crear-lista-buena-fe.html')

    @app.route('/jugadores')
    @login_required
    def jugadores():
        return render_template('jugadores.html')

    @app.route('/equipos-categorias')
    @login_required
    def equipos_categorias():
        return render_template('equipos-categorias.html')

    @app.route('/datos-club')
    @login_required
    def datos_club():
        return render_template('datos-club.html')

    @app.route('/carga-incidencias')
    @login_required
    def carga_incidencias():
        return render_template('carga-incidencias.html')

    @app.route('/cuerpo-tecnico')
    @login_required
    def cuerpo_tecnico():
        return render_template('cuerpo-tecnico.html')

    @app.route('/control-partido')
    @login_required
    def control_partido():
        return render_template('control-partido.html')

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

    app.view_functions['carga_incidencias'] = require_permission('puede_cargar_incidencias')(app.view_functions['carga_incidencias'])
    app.view_functions['precarga_equipos'] = require_permission('puede_precargar_equipos')(app.view_functions['precarga_equipos'])

    @app.after_request
    def set_security_headers(resp):
        resp.headers.setdefault('X-Content-Type-Options', 'nosniff')
        resp.headers.setdefault('X-Frame-Options', 'DENY')
        resp.headers.setdefault('Referrer-Policy', 'no-referrer-when-downgrade')
        try:
            if request.is_secure or app.config.get('SESSION_COOKIE_SECURE'):
                resp.headers.setdefault('Strict-Transport-Security', 'max-age=31536000; includeSubDomains')
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

    return app


app = create_app()

__all__ = ["create_app", "app", "db", "login_manager", "csrf"]
