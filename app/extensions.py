"""Extensiones Flask inicializadas una sola vez.

Se exportan desde `app.__init__` para compatibilidad con imports existentes.
"""

import logging
import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def init_extensions(app) -> None:
    db.init_app(app)
    migrate.init_app(app, db)

    if os.getenv('ENABLE_CSRF', 'true').lower() == 'true':
        csrf.init_app(app)
        logging.getLogger(__name__).info('CSRF protection habilitado.')
    else:
        logging.getLogger(__name__).info('CSRF protection deshabilitado.')
