# generar_backups.ps1

# 1. Obtener la fecha y hora actual para el nombre del archivo
$fecha = Get-Date -Format "yyyyMMdd_HHmmss"
$carpetaDestino = ".\backups"

# 2. Crear la carpeta "backups" si no existe
if (-not (Test-Path -Path $carpetaDestino)) {
    New-Item -ItemType Directory -Path $carpetaDestino | Out-Null
    Write-Host "Carpeta 'backups' creada."
}

Write-Host "Iniciando respaldo de las bases de datos..." -ForegroundColor Cyan

# 3. Backup de MariaDB
Write-Host "-> Respaldando MariaDB..."
docker compose --project-directory . -f docker/docker-compose.yml exec mariadb sh -c "mariadb-dump -u hockeyuser -phockeypass hockey > /tmp/backup_mariadb.sql"
docker compose --project-directory . -f docker/docker-compose.yml cp mariadb:/tmp/backup_mariadb.sql "$carpetaDestino\mariadb_$fecha.sql"

# 4. Backup de MongoDB
Write-Host "-> Respaldando MongoDB..."
docker compose --project-directory . -f docker/docker-compose.yml exec mongodb sh -c "mongodump --username admin --password adminpass --authenticationDatabase admin --db hockey --archive=/tmp/backup_mongodb.archive"
docker compose --project-directory . -f docker/docker-compose.yml cp mongodb:/tmp/backup_mongodb.archive "$carpetaDestino\mongodb_$fecha.archive"

Write-Host "¡Backups generados con exito en la carpeta '$carpetaDestino'!" -ForegroundColor Green