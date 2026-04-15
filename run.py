import os
from app import app

if __name__ == "__main__":
    # En contenedores, exponer en 0.0.0.0 para que sea accesible desde el host
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    # Controlar debug vía variable (por defecto deshabilitado en producción)
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)