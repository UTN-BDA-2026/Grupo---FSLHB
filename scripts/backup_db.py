import os
import subprocess
import shlex
from datetime import datetime


def get_db_url() -> str:
    return os.getenv('DATABASE_URL') or os.getenv('PROD_DATABASE_URI') or os.getenv('DEV_DATABASE_URI')


def backup(output_dir: str = 'backups') -> str:
    db_url = get_db_url()
    if not db_url:
        raise RuntimeError('No hay DATABASE_URL/PROD_DATABASE_URI/DEV_DATABASE_URI definido en el entorno.')

    os.makedirs(output_dir, exist_ok=True)
    ts = datetime.utcnow().strftime('%Y%m%d-%H%M%S')
    out_file = os.path.join(output_dir, f'hockey-{ts}.dump')

    # Requiere pg_dump en PATH
    cmd = f"pg_dump --format=custom --file={shlex.quote(out_file)} {shlex.quote(db_url)}"
    print(f"Ejecutando: {cmd}")
    subprocess.check_call(cmd, shell=True)
    print(f"Backup OK: {out_file}")
    return out_file


if __name__ == '__main__':
    backup()
