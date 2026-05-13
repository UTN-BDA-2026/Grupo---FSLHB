"""
Script de inicialización completo del proyecto Hockey Acción con MongoDB.

Ejecuta todas las tareas necesarias para preparar la base de datos:
1. Verifica conexión a MongoDB
2. Crea índices en colecciones críticas
3. (Opcional) Crea usuario admin inicial
4. (Opcional) Carga datos de ejemplo

Uso:
    python scripts/init_project.py                          # Inicialización completa interactiva
    python scripts/init_project.py --skip-indexes           # Sin crear índices
    python scripts/init_project.py --create-admin           # Crear usuario admin
    python scripts/init_project.py --all                    # Todo automático

Exit codes:
    0 = Éxito
    1 = Error de conexión
    2 = Error en índices
    3 = Error al crear usuario
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Tuple

# Agregar app al path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app import app
from app.extensions import mongo
from app.models.usuario import Usuario
from app.models.club import Club
from app.repositories.usuario_repositorio import UsuarioRepositorio
from app.repositories.club_repositorio import ClubRepository
from app.services.usuario_service import UsuarioService


def print_header(title: str) -> None:
    """Imprime un encabezado de sección."""
    print("\n" + "=" * 70)
    print(f"🏒 {title}")
    print("=" * 70)


def check_mongodb_connection() -> Tuple[bool, str]:
    """Verifica la conexión a MongoDB."""
    try:
        mongo.db.command('ping')
        return True, "✅ Conexión a MongoDB exitosa"
    except Exception as e:
        return False, f"❌ Error de conexión a MongoDB: {str(e)}"


def run_indexes() -> bool:
    """Ejecuta el setup de índices."""
    print_header("INICIALIZANDO ÍNDICES")
    
    try:
        # Importar y ejecutar el script de índices
        from setup_mongodb_indexes import create_collection_indexes, check_mongodb_connection as check_conn
        
        db = mongo.db
        connected, msg = check_conn(db)
        if not connected:
            print(f"❌ {msg}")
            return False
        
        print(f"✅ {msg}")
        created, skipped, errors = create_collection_indexes(db)
        
        print(f"\n📊 Resumen de índices:")
        print(f"  ✓ Creados: {created}")
        print(f"  ⏭️  Existentes: {skipped}")
        
        if errors:
            print(f"  ❌ Errores: {len(errors)}")
            for error in errors:
                print(f"     - {error}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def create_admin_user() -> bool:
    """Crea un usuario admin inicial."""
    print_header("CREAR USUARIO ADMIN")
    
    try:
        with app.app_context():
            # Verificar si ya existe un admin
            admin_exists = UsuarioRepositorio._col().find_one({'is_admin': True})
            if admin_exists:
                print("⏭️  Ya existe un usuario admin en la base de datos. Saltando...")
                return True
            
            # Solicitar datos
            username = input("👤 Nombre de usuario admin: ").strip()
            if not username:
                print("❌ Nombre de usuario vacío")
                return False
            
            # Verificar si existe
            if UsuarioRepositorio.buscar_por_username(username):
                print(f"❌ El usuario '{username}' ya existe")
                return False
            
            password = input("🔐 Contraseña: ").strip()
            if not password:
                print("❌ Contraseña vacía")
                return False
            
            ok, msg = UsuarioService.validar_password(password)
            if not ok:
                print(f"❌ {msg}")
                return False
            
            # Crear usuario
            hashed_pw = UsuarioService.hashear_password(password)
            admin_user = Usuario(
                username=username,
                password=hashed_pw,
                is_admin=True,
                is_operador=True,
                puede_cargar_incidencias=True,
                puede_precargar_equipos=True
            )
            
            admin_user = UsuarioRepositorio.crear(admin_user)
            print(f"✅ Usuario admin '{username}' creado exitosamente")
            print(f"   ID: {admin_user._id}")
            return True
            
    except KeyboardInterrupt:
        print("\n⚠️  Cancelado por el usuario")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def create_sample_club() -> bool:
    """Crea un club de ejemplo."""
    print_header("CREAR CLUB DE EJEMPLO")
    
    try:
        with app.app_context():
            # Verificar si existe
            if ClubRepository.buscar_por_nombre("Club Ejemplo"):
                print("⏭️  Club de ejemplo ya existe. Saltando...")
                return True
            
            club = Club(
                nombre="Club Ejemplo",
                razon_social="Club Ejemplo S.A.",
                contacto="Juan Pérez",
                email="contacto@clubejemplo.com",
                domicilio="Calle Principal 123",
                telefono="+54 9 2664 123456",
                web="https://clubejemplo.com"
            )
            
            club = ClubRepository.crear(club)
            print(f"✅ Club '{club.nombre}' creado exitosamente")
            print(f"   ID: {club._id}")
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def log_initialization_report() -> None:
    """Genera un reporte de inicialización."""
    print_header("RESUMEN DE INICIALIZACIÓN")
    
    with app.app_context():
        db = mongo.db
        
        # Contar documentos
        collections_count = {}
        for collection_name in ['usuarios', 'clubes', 'equipos', 'partidos', 'noticias']:
            try:
                count = db[collection_name].count_documents({})
                collections_count[collection_name] = count
            except:
                collections_count[collection_name] = 0
        
        print(f"\n📊 Estado de colecciones:")
        for collection, count in collections_count.items():
            status = "✅" if count > 0 else "⚠️ "
            print(f"  {status} {collection}: {count} documentos")
        
        print(f"\n⏰ Inicialización completada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Inicializa el proyecto Hockey Acción con MongoDB',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python scripts/init_project.py                 # Modo interactivo
  python scripts/init_project.py --all           # Automatizado (índices + admin)
  python scripts/init_project.py --create-admin  # Solo crear admin
        """
    )
    parser.add_argument('--skip-indexes', action='store_true', help='No crear índices')
    parser.add_argument('--create-admin', action='store_true', help='Crear usuario admin')
    parser.add_argument('--all', action='store_true', help='Ejecutar todo de forma automatizada')
    
    args = parser.parse_args()
    
    print_header("INICIALIZACIÓN - HOCKEY ACCIÓN")
    

    
    try:
        # 1. Verificar conexión
        connected, msg = check_mongodb_connection()
        print(msg)
        if not connected:
            return 1
        
        # 2. Índices
        if not args.skip_indexes:
            if not run_indexes():
                return 2
        
        # 3. Usuario admin (interactivo o automático)
        if args.create_admin or args.all:
            if not create_admin_user():
                return 3
        
        # 4. Club de ejemplo (solo en modo --all)
        if args.all:
            if not create_sample_club():
                print("⚠️  Error al crear club de ejemplo (no crítico)")
        
        # 5. Reporte final
        log_initialization_report()
        
        print("\n✅ Inicialización completada exitosamente")
        print("\n📝 Próximos pasos:")
        print("   1. Acceder a http://localhost:5000")
        print("   2. Loguearse con el usuario admin creado")
        print("   3. Comenzar a cargar datos")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Inicialización cancelada por el usuario")
        return 130
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
