"""
Script de verificación previa para asegurar que todo está configurado correctamente.

Verifica:
1. Archivo .env existe
2. Variables de entorno críticas
3. MongoDB accesible
4. Colecciones bases creadas
5. Índices creados

Uso:
    python scripts/verify_setup.py

Exit codes:
    0 = Todo OK
    1 = Error crítico
    2 = Advertencias (no crítico)
"""

import sys
import os
from pathlib import Path
from typing import List, Tuple

# Agregar app al path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault('FLASK_ENV', 'development')

from app import app
from app.extensions import mongo


def check_env_file() -> Tuple[bool, str]:
    """Verifica que el archivo .env existe."""
    env_path = REPO_ROOT / '.env'
    if env_path.exists():
        return True, "✅ Archivo .env encontrado"
    else:
        return False, "❌ Archivo .env NO encontrado"


def check_required_env_vars() -> Tuple[bool, List[str]]:
    """Verifica variables de entorno críticas."""
    required = ['FLASK_ENV', 'MONGO_URI', 'SECRET_KEY']
    missing = []
    
    for var in required:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        return False, missing
    else:
        return True, []


def check_mongodb_connection() -> Tuple[bool, str]:
    """Verifica conexión a MongoDB."""
    try:
        mongo.db.command('ping')
        return True, "✅ MongoDB accesible"
    except Exception as e:
        return False, f"❌ MongoDB NO accesible: {str(e)}"


def check_collections_exist() -> Tuple[bool, dict]:
    """Verifica que las colecciones existen."""
    critical = ['usuarios', 'clubes', 'equipos', 'partidos']
    
    db = mongo.db
    existing_critical = []
    missing_critical = []
    
    for col_name in critical:
        try:
            count = db[col_name].count_documents({})
            if count >= 0:  # Existe si el conteo funciona
                existing_critical.append(col_name)
        except:
            missing_critical.append(col_name)
            raise
    
    return len(missing_critical) == 0, {
        'critical': {'existing': existing_critical, 'missing': missing_critical},
    }


def check_indexes() -> Tuple[bool, dict]:
    """Verifica que los índices están creados."""
    key_indexes = {
        'usuarios': ['username_1'],
        'clubes': ['nombre_1'],
        'equipos': ['nombre_1'],
        'partidos': ['fecha_-1', 'torneo_id_1'],
    }
    
    db = mongo.db
    status = {}
    all_ok = True
    
    for collection_name, expected_indexes in key_indexes.items():
        try:
            indexes = db[collection_name].index_information()
            missing = []
            
            for exp_idx in expected_indexes:
                if exp_idx not in indexes:
                    missing.append(exp_idx)
            
            if missing:
                all_ok = False
                status[collection_name] = f"❌ Faltan: {', '.join(missing)}"
            else:
                status[collection_name] = "✅"
        except Exception as e:
            all_ok = False
            status[collection_name] = f"⚠️  Error: {str(e)}"
    
    return all_ok, status


def print_section(title: str) -> None:
    """Imprime un título de sección."""
    print(f"\n{'=' * 60}")
    print(f"🔍 {title}")
    print('=' * 60)


def main():
    """Función principal."""
    
    print_section("VERIFICACIÓN DE SETUP - HOCKEY ACCIÓN")
    
    errors = []
    warnings = []
    
    # 1. Verificar .env
    print("\n📋 Verificando archivo configuración...")
    ok, msg = check_env_file()
    print(f"  {msg}")
    if not ok:
        errors.append("Falta archivo .env")
    
    # 2. Variables de entorno
    print("\n🔑 Verificando variables de entorno...")
    ok, missing = check_required_env_vars()
    if ok:
        print("  ✅ Todas las variables críticas definidas")
    else:
        msg = f"❌ Variables faltantes: {', '.join(missing)}"
        print(f"  {msg}")
        errors.append(msg)
    
    # 3. MongoDB
    print("\n🗄️  Verificando MongoDB...")
    with app.app_context():
        ok, msg = check_mongodb_connection()
        print(f"  {msg}")
        if not ok:
            errors.append("No se puede conectar a MongoDB")
        
        # 4. Colecciones
        if not errors:
            print("\n📦 Verificando colecciones...")
            ok, collections_info = check_collections_exist()
            critical = collections_info['critical']
            
            if critical['existing']:
                print(f"  ✅ Colecciones existentes: {', '.join(critical['existing'])}")
            
            if critical['missing']:
                msg = f"⚠️  Colecciones faltantes: {', '.join(critical['missing'])}"
                print(f"  {msg}")
                warnings.append(msg)
            
            # 5. Índices
            print("\n📇 Verificando índices...")
            ok, indexes_info = check_indexes()
            
            for collection, status in indexes_info.items():
                prefix = "  "
                print(f"{prefix}{collection}: {status}")
            
            if not ok:
                warnings.append("Algunos índices no están creados")
    
    # Resumen
    print_section("RESUMEN")
    
    if not errors and not warnings:
        print("\n✅ TODO OK - El proyecto está listo para ejecutarse")
        print("\nComandos para arrancar:")
        print("  docker compose up --build")
        print("\nOpcional (crear índices):")
        print("  docker compose exec app python scripts/setup_mongodb_indexes.py")
        print("\nOpcional (inicialización completa):")
        print("  docker compose exec app python scripts/init_project.py --all")
        return 0
    
    if errors:
        print("\n❌ ERRORES CRÍTICOS:")
        for i, error in enumerate(errors, 1):
            print(f"   {i}. {error}")
    
    if warnings:
        print("\n⚠️  ADVERTENCIAS (no crítico):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
        
        if not errors:
            print("\n✅ Puedes arrancar, pero considera ejecutar:")
            print("   docker compose exec app python scripts/init_project.py --all")
            return 2  # Advertencia
    
    return 1 if errors else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚠️  Verificación cancelada")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
