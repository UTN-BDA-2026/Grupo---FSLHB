import os
import sys

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app import create_app, db


def main() -> int:
    uri = os.environ.get("PROD_DATABASE_URI")
    if not uri:
        print("PROD_DATABASE_URI env var is required (point it to MariaDB).", file=sys.stderr)
        return 1

    app = create_app("production")
    with app.app_context():
        # Ensure models are imported so tables are registered
        import app.models  # noqa: F401

        db.create_all()
        print("Schema created/verified using db.create_all().")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
