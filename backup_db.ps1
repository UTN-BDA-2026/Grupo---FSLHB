# Backup de la base de datos Postgres en Docker
# Guarda el backup en la carpeta backups/ con fecha y hora en el nombre

$fecha = Get-Date -Format "yyyy-MM-dd_HHmm"
$backupDir = "backups"
$backupFile = "backup_$fecha.sql"
$fullPath = Join-Path $backupDir $backupFile

# Crear carpeta backups si no existe
if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
}

# Ejecutar el backup usando docker-compose y pg_dump
# Cambia "db" si tu servicio de base de datos tiene otro nombre en docker-compose.yml
# Cambia "hockeyuser" y "hockey" si tu usuario/db son distintos

docker-compose exec db pg_dump -U hockeyuser -d hockey > $fullPath

Write-Host "Backup realizado: $fullPath"