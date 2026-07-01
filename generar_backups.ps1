# generar_backups.ps1

param(
    [switch]$ValidateRestore
)

$fecha = Get-Date -Format "yyyyMMdd_HHmmss"
$carpetaDestino = ".\backups"
$maxBackups = 3

if (-not (Test-Path -Path $carpetaDestino)) {
    New-Item -ItemType Directory -Path $carpetaDestino -Force | Out-Null
    Write-Host "Carpeta 'backups' creada." -ForegroundColor Green
}

Write-Host "Iniciando respaldo de las bases de datos..." -ForegroundColor Cyan

Write-Host "-> Respaldando MariaDB..."
docker compose --project-directory . -f docker/docker-compose.yml exec -T mariadb sh -c "mariadb-dump -u hockeyuser -phockeypass hockey > /tmp/backup_mariadb.sql"
docker compose --project-directory . -f docker/docker-compose.yml cp mariadb:/tmp/backup_mariadb.sql "$carpetaDestino\mariadb_$fecha.sql"

Write-Host "-> Respaldando MongoDB..."
docker compose --project-directory . -f docker/docker-compose.yml exec -T mongodb sh -c "mongodump --username admin --password adminpass --authenticationDatabase admin --db hockey --archive=/tmp/backup_mongodb.archive"
docker compose --project-directory . -f docker/docker-compose.yml cp mongodb:/tmp/backup_mongodb.archive "$carpetaDestino\mongodb_$fecha.archive"

Write-Host "¡Backups generados con exito en la carpeta '$carpetaDestino'!" -ForegroundColor Green

Write-Host "-> Aplicando política de retención: conservar los últimos $maxBackups backups por tipo..."
$mariadbBackups = Get-ChildItem "$carpetaDestino\mariadb_*.sql" -File | Sort-Object LastWriteTimeUtc
$mongoBackups = Get-ChildItem "$carpetaDestino\mongodb_*.archive" -File | Sort-Object LastWriteTimeUtc

if ($mariadbBackups.Count -gt $maxBackups) {
    $oldMariaDB = $mariadbBackups | Select-Object -First ($mariadbBackups.Count - $maxBackups)
    $oldMariaDB | ForEach-Object { Remove-Item $_.FullName -Force; Write-Host "   Eliminado backup antiguo de MariaDB: $($_.Name)" }
}

if ($mongoBackups.Count -gt $maxBackups) {
    $oldMongo = $mongoBackups | Select-Object -First ($mongoBackups.Count - $maxBackups)
    $oldMongo | ForEach-Object { Remove-Item $_.FullName -Force; Write-Host "   Eliminado backup antiguo de MongoDB: $($_.Name)" }
}

function Test-MariaDBRestore {
    param([string]$BackupFile)

    Write-Host "-> Validando restauración de MariaDB..." -ForegroundColor Yellow

    if (-not (Test-Path -Path $BackupFile)) {
        Write-Host "   ✗ No se encontró el backup de MariaDB: $BackupFile" -ForegroundColor Red
        return $false
    }

    $tempContainerName = "mariadb-validate-$([int64](Get-Date -UFormat %s))"

    try {
        Write-Host "   Iniciando contenedor temporal: $tempContainerName"
        docker run -d --name $tempContainerName -e MARIADB_ROOT_PASSWORD=test -e MARIADB_DATABASE=hockey -e MARIADB_USER=testuser -e MARIADB_PASSWORD=testpass mariadb:10.11 | Out-Null
        Start-Sleep -Seconds 10

        docker cp $BackupFile "$tempContainerName`:/tmp/backup.sql" 2>$null | Out-Null
        docker exec $tempContainerName sh -c "mariadb -uroot -ptest hockey < /tmp/backup.sql" 2>$null | Out-Null

        docker exec $tempContainerName sh -c "printf 'SHOW TABLES;' > /tmp/validate.sql" 2>$null | Out-Null
        $tableOutput = docker exec $tempContainerName sh -c "mariadb -uroot -ptest hockey < /tmp/validate.sql" 2>$null
        $tableLines = @($tableOutput -split "`n" | Where-Object { $_.Trim() })
        if ($tableLines.Count -gt 0) {
            Write-Host "   [OK] MariaDB validado: $($tableLines.Count) tablas encontradas" -ForegroundColor Green
            return $true
        }

        Write-Host "   [FAIL] MariaDB validación fallida: no se encontraron tablas" -ForegroundColor Red
        return $false
    }
    catch {
        Write-Host "   [FAIL] Error al validar MariaDB: $_" -ForegroundColor Red
        return $false
    }
    finally {
        docker rm -f $tempContainerName 2>$null | Out-Null
    }
}

function Test-MongoDBRestore {
    param([string]$BackupFile)

    Write-Host "-> Validando restauración de MongoDB..." -ForegroundColor Yellow

    if (-not (Test-Path -Path $BackupFile)) {
        Write-Host "   ✗ No se encontró el backup de MongoDB: $BackupFile" -ForegroundColor Red
        return $false
    }

    $tempContainerName = "mongodb-validate-$([int64](Get-Date -UFormat %s))"

    try {
        Write-Host "   Iniciando contenedor temporal: $tempContainerName"
        docker run -d --name $tempContainerName -e MONGO_INITDB_ROOT_USERNAME=admin -e MONGO_INITDB_ROOT_PASSWORD=adminpass mongo:7 | Out-Null
        Start-Sleep -Seconds 10

        docker cp $BackupFile "$tempContainerName`:/tmp/backup.archive" 2>$null | Out-Null
        docker exec $tempContainerName sh -c "mongorestore --username admin --password adminpass --authenticationDatabase admin --archive=/tmp/backup.archive" 2>$null | Out-Null

        Write-Host "   [OK] MongoDB validado: restauración completada" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "   [FAIL] Error al validar MongoDB: $_" -ForegroundColor Red
        return $false
    }
    finally {
        docker rm -f $tempContainerName 2>$null | Out-Null
    }
}

if ($ValidateRestore) {
    Write-Host "`nIniciando validación de restauraciones..." -ForegroundColor Cyan

    $mariadbBackup = "$carpetaDestino\mariadb_$fecha.sql"
    $mongodbBackup = "$carpetaDestino\mongodb_$fecha.archive"

    $mariadbValid = Test-MariaDBRestore -BackupFile $mariadbBackup
    $mongodbValid = Test-MongoDBRestore -BackupFile $mongodbBackup

    Write-Host "`nResultados de validación:" -ForegroundColor Cyan
    Write-Host "  MariaDB: $(if ($mariadbValid) { 'OK' } else { 'FALLO' })"
    Write-Host "  MongoDB: $(if ($mongodbValid) { 'OK' } else { 'FALLO' })"

    if ($mariadbValid -and $mongodbValid) {
        Write-Host "`n[OK] Todos los backups se validaron correctamente" -ForegroundColor Green
    }
    else {
        Write-Host "`n[FAIL] Algunos backups tienen problemas" -ForegroundColor Red
        exit 1
    }
}