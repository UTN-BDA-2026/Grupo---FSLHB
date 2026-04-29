"""Configuración de la aplicación (env, DB URI, cookies, CORS)."""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask_cors import CORS


def load_env_file() -> None:
    basedir = Path(__file__).resolve().parents[1]
    env_path = os.path.join(basedir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)


def apply_app_config(app, config_name: str | None = None) -> str:
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

    is_debug = app.debug or os.getenv('FLASK_DEBUG', '0') in (
        '1',
        'true',
        'True',
    ) or os.getenv('DEBUG', '0') in ('1', 'true', 'True')

    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    app.config['SESSION_COOKIE_SECURE'] = (
        os.getenv('SESSION_COOKIE_SECURE', 'true' if not is_debug else 'false').lower()
        == 'true'
    )
    app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {'pool_pre_ping': True})

    return config_name


def init_cors(app, config_name: str) -> None:
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
