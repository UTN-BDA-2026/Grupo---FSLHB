from app.auth import require_admin
from app.extensions import csrf, mongo, login_manager
from app.factory import create_app

app = create_app()

__all__ = [
    "create_app",
    "app",
    "mongo",
    "login_manager",
    "csrf",
    "require_admin",
]