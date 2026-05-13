#!/bin/bash
# Script de inicialización rápida para Docker
# Ejecuta todos los pasos necesarios después de que Docker Compose levanta

set -e  # Exit on error

echo "=================================="
echo "🏒 HOCKEY ACCIÓN - INICIALIZACIÓN"
echo "=================================="
echo ""

# Esperar a que MongoDB esté listo
echo "⏳ Esperando a que MongoDB esté listo..."
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if python scripts/verify_setup.py 2>/dev/null; then
        echo "✅ MongoDB listo"
        break
    fi
    attempt=$((attempt + 1))
    echo "   Intento $attempt/$max_attempts..."
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "❌ Timeout esperando MongoDB"
    exit 1
fi

echo ""
echo "🔍 Verificando setup..."
python scripts/verify_setup.py
echo ""

echo "📦 Creando índices..."
python scripts/setup_mongodb_indexes.py
echo ""

echo "✅ Proyecto inicializado correctamente"
echo ""
echo "🚀 Acceder a: http://localhost:5000"
echo ""
