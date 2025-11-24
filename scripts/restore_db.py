import os
import subprocess
import shlex
import sys


def get_db_url() -> str:
    return os.getenv('DATABASE_URL') or os.getenv('PROD_DATABASE_URI') or os.getenv('DEV_DATABASE_URI')


def restore(dump_file: str):
    if not os.path.exists(dump_file):
        raise FileNotFoundError(dump_file)
    db_url = get_db_url()
    if not db_url:
        raise RuntimeError('No hay DATABASE_URL/PROD_DATABASE_URI/DEV_DATABASE_URI definido en el entorno.')

    # Requiere pg_restore
    cmd = f"pg_restore --clean --if-exists --no-owner --no-privileges --dbname={shlex.quote(db_url)} {shlex.quote(dump_file)}"
    print(f"Ejecutando: {cmd}")
    subprocess.check_call(cmd, shell=True)
    print("Restore OK")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python scripts/restore_db.py ruta/al/archivo.dump")
        sys.exit(1)
    restore(sys.argv[1])
