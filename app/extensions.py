"""Extensiones Flask inicializadas una sola vez.

Se exportan desde `app.__init__` para compatibilidad con imports existentes.
"""

import logging
import os

from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


mongo = PyMongo()
login_manager = LoginManager()
csrf = CSRFProtect()


def init_extensions(app) -> None:
    mongo.init_app(app)

    if os.getenv('ENABLE_CSRF', 'true').lower() == 'true':
        csrf.init_app(app)
        logging.getLogger(__name__).info('CSRF protection habilitado.')
    else:
        logging.getLogger(__name__).info('CSRF protection deshabilitado.')
