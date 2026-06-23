"""Application factory.

Deja `app.__init__` liviano y mantiene compatibilidad con `from app import create_app`.
"""

import json
from bson import ObjectId
from flask import Flask
from flask.json.provider import DefaultJSONProvider


class MongoJSONProvider(DefaultJSONProvider):
    """JSON Provider que serializa ObjectId de MongoDB."""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)


def create_app(config_name: str | None = None) -> Flask:
    from app.app_config import apply_app_config, init_cors, load_env_file
    from app.auth import apply_static_page_permissions, init_login
    from app.blueprints import ALL_BLUEPRINTS
    from app.extensions import init_extensions
    from app.hooks import (
        register_error_handlers,
        register_https_enforcement,
        register_security_headers,
    )

    app = Flask(__name__)
    
    # Configurar JSON provider personalizado para serializar ObjectId
    app.json = MongoJSONProvider(app)

    load_env_file()
    effective_config_name = apply_app_config(app, config_name)

    init_extensions(app)
    init_cors(app, effective_config_name)

    # Asegurar tablas SQL necesarias (MariaDB) para modelos SQLAlchemy.
    from app.extensions import db
    from app.models.jugadora import Jugadora  # noqa: F401
    with app.app_context():
        db.create_all()

    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)

    init_login(app)
    apply_static_page_permissions(app)

    register_security_headers(app)
    register_error_handlers(app)
    register_https_enforcement(app)

    return app
