from app.auth import require_admin
from app.extensions import csrf, db, login_manager, migrate
from app.factory import create_app

app = create_app()

__all__ = [
    "create_app",
    "app",
    "db",
    "login_manager",
    "csrf",
    "migrate",
    "require_admin",
]