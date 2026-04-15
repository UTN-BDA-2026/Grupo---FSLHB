# Backups de la base de datos (PostgreSQL)

Estos scripts usan `pg_dump` y `pg_restore`. Asegúrate de tener instaladas las utilidades de PostgreSQL en tu PATH.

## Variables de entorno necesarias

Define una de las siguientes (en este orden de prioridad):

- `DATABASE_URL`
- `PROD_DATABASE_URI`
- `DEV_DATABASE_URI`

Ejemplo (PowerShell):

```powershell
$env:DATABASE_URL = "postgresql://hockeyuser:hockeypass@localhost:5433/hockey"
```

## Crear un backup

```powershell
python scripts/backup_db.py
```

Se generará un archivo `.dump` en la carpeta `backups/`.

## Restaurar un backup

```powershell
python scripts/restore_db.py .\backups\hockey-YYYYMMDD-HHMMSS.dump
```

> Nota: `--clean --if-exists` intenta dropear objetos antes de crearlos. Úsalo con precaución en producción.
