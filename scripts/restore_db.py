import os
import subprocess
import shlex
import sys


def get_db_url() -> str:
    return os.getenv('DATABASE_URL') or os.getenv('PROD_DATABASE_URI') or os.getenv('DEV_DATABASE_URI')


def restore(dump_file: str):
    if not os.path.exists(dump_file):
        raise FileNotFoundError(dump_file)

    # En Windows, docker compose exec con stdin puede tener problemas
    # Por eso copiamos el archivo al contenedor y lo restauramos desde allí
    
    # 1. Copiar el dump al contenedor
    cp_cmd = [
        'docker', 'compose', '--project-directory', '.', '-f', 'docker/docker-compose.yml',
        'cp', dump_file, 'db:/tmp/backup.dump'
    ]
    print("Copiando dump al contenedor...")
    print('Comando:', ' '.join(shlex.quote(c) for c in cp_cmd))
    subprocess.check_call(cp_cmd)
    
    # 2. Restaurar dentro del contenedor
    restore_cmd = [
        'docker', 'compose', '--project-directory', '.', '-f', 'docker/docker-compose.yml',
        'exec', '-T', 'db',
        'pg_restore', '--clean', '--if-exists', '--no-owner', '--no-privileges',
        '-U', 'hockeyuser', '-d', 'hockey', '/tmp/backup.dump'
    ]
    print("Restaurando base dentro del contenedor 'db' con pg_restore...")
    print('Comando:', ' '.join(shlex.quote(c) for c in restore_cmd))
    subprocess.check_call(restore_cmd)
    print("Restore OK")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python scripts/restore_db.py ruta/al/archivo.dump")
        sys.exit(1)
    restore(sys.argv[1])
