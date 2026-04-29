"""Application factory.

Deja `app.__init__` liviano y mantiene compatibilidad con `from app import create_app`.
"""

from flask import Flask


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

    load_env_file()
    effective_config_name = apply_app_config(app, config_name)

    init_extensions(app)
    init_cors(app, effective_config_name)

    for bp in ALL_BLUEPRINTS:
        app.register_blueprint(bp)

    init_login(app)
    apply_static_page_permissions(app)

    register_security_headers(app)
    register_error_handlers(app)
    register_https_enforcement(app)

    return app
