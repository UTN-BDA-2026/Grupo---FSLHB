import os
import subprocess
import shlex
import sys


def get_db_url() -> str:
    return os.getenv('DATABASE_URL') or os.getenv('PROD_DATABASE_URI') or os.getenv('DEV_DATABASE_URI')


def restore(dump_file: str):
    if not os.path.exists(dump_file):
        raise FileNotFoundError(dump_file)

    # En este proyecto la base corre en Docker (servicio "db").
    # Usamos pg_restore dentro del contenedor para no depender de
    # tener las herramientas de PostgreSQL instaladas en Windows.
    cmd = [
        'docker-compose', 'exec', '-T', 'db',
        'pg_restore', '--clean', '--if-exists', '--no-owner', '--no-privileges',
        '-U', 'hockeyuser', '-d', 'hockey', '-'
    ]
    print("Restaurando base dentro del contenedor 'db' con pg_restore...")
    print('Comando:', ' '.join(shlex.quote(c) for c in cmd))
    with open(dump_file, 'rb') as f:
        subprocess.check_call(cmd, stdin=f)
    print("Restore OK")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python scripts/restore_db.py ruta/al/archivo.dump")
        sys.exit(1)
    restore(sys.argv[1])
