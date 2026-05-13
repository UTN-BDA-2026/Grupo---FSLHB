"""
Inicializa y verifica índices de MongoDB para optimizar búsquedas.

Este script debe ejecutarse una sola vez después de crear la base de datos.

Uso:
    python scripts/setup_mongodb_indexes.py              # Crear índices
    python scripts/setup_mongodb_indexes.py --reset      # Resetear todos los índices
    python scripts/setup_mongodb_indexes.py --verify     # Solo verificar índices existentes

Índices creados:
    - usuarios: username (único)
    - clubes: nombre (único)
    - equipos: nombre (único)
    - partidos: fecha, torneo_id
    - incidencias: partido_id, jugadora_id
    - noticias: fecha
    - torneo: nombre (único)
    - jugadora: nombre
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Agregar app al path
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from app import app
from app.extensions import mongo


def get_existing_indexes(collection):
    """Obtiene índices existentes en una colección."""
    return collection.index_information()


def create_collection_indexes(db):
    """Crea índices optimizados en todas las colecciones críticas."""
    indexes_created = 0
    indexes_skipped = 0
    errors = []

    collections_config = [
        # (nombre_colección, [(campos, opciones), ...])
        ('usuarios', [
            (([('username', 1)], {'unique': True}), 'Username único'),
            (([('is_admin', 1)], {}), 'Búsqueda de admins'),
            (([('is_operador', 1)], {}), 'Búsqueda de operadores'),
        ]),
        ('clubes', [
            (([('nombre', 1)], {'unique': True}), 'Nombre único'),
        ]),
        ('equipos', [
            (([('nombre', 1)], {'unique': True}), 'Nombre único'),
            (([('club_id', 1)], {}), 'Búsqueda por club'),
        ]),
        ('partidos', [
            (([('fecha', -1)], {}), 'Ordena por fecha (reciente primero)'),
            (([('torneo_id', 1)], {}), 'Búsqueda por torneo'),
            (([('equipo_local_id', 1)], {}), 'Búsqueda por equipo local'),
            (([('equipo_visitante_id', 1)], {}), 'Búsqueda por equipo visitante'),
        ]),
        ('incidencias', [
            (([('partido_id', 1)], {}), 'Búsqueda por partido'),
            (([('jugadora_id', 1)], {}), 'Búsqueda por jugadora'),
            (([('tipo_incidencia', 1)], {}), 'Búsqueda por tipo de incidencia'),
        ]),
        ('noticias', [
            (([('fecha', -1)], {}), 'Ordena por fecha (reciente primero)'),
        ]),
        ('torneo', [
            (([('nombre', 1)], {'unique': True}), 'Nombre único'),
        ]),
        ('jugadora', [
            (([('nombre', 1)], {}), 'Búsqueda por nombre'),
            (([('club_id', 1)], {}), 'Búsqueda por club'),
        ]),
    ]

    for collection_name, index_list in collections_config:
        try:
            collection = db[collection_name]
            existing_indexes = get_existing_indexes(collection)
            
            print(f"\n📋 Colección: {collection_name}")
            
            for (fields, options), description in index_list:
                tuple(fields)
                
                # Verificar si el índice ya existe
                index_exists = False
                for existing_index_name, existing_index_info in existing_indexes.items():
                    if existing_index_info['key'] == list(fields):
                        index_exists = True
                        print(f"  ⏭️  {description} (ya existe)")
                        indexes_skipped += 1
                        break
                
                if not index_exists:
                    collection.create_index(fields, **options)
                    print(f"  ✓  {description}")
                    indexes_created += 1
                    
        except Exception as e:
            error_msg = f"Error en colección '{collection_name}': {str(e)}"
            errors.append(error_msg)
            print(f"  ❌ {error_msg}")

    return indexes_created, indexes_skipped, errors


def reset_indexes(db):
    """Elimina todos los índices (excepto _id) de colecciones críticas."""
    print("\n⚠️  Reseteando índices...")
    collections = ['usuarios', 'clubes', 'equipos', 'partidos', 'incidencias', 'noticias', 'torneo', 'jugadora']
    
    for collection_name in collections:
        try:
            collection = db[collection_name]
            # drop_index() borra un índice por nombre, drop_indexes() borra todos excepto _id
            collection.drop_indexes()
            print(f"  ✓ Índices eliminados en {collection_name}")
        except Exception as e:
            print(f"  ⚠️  {collection_name}: {str(e)}")


def verify_indexes(db):
    """Verifica y muestra los índices existentes."""
    collections = ['usuarios', 'clubes', 'equipos', 'partidos', 'incidencias', 'noticias', 'torneo', 'jugadora']
    
    print("\n🔍 Índices actuales en MongoDB:")
    
    for collection_name in collections:
        try:
            collection = db[collection_name]
            indexes = get_existing_indexes(collection)
            
            if indexes:
                print(f"\n  📋 {collection_name}:")
                for index_name, index_info in indexes.items():
                    fields = ', '.join([f"{k} ({v})" for k, v in index_info['key']])
                    unique = " (único)" if index_info.get('unique', False) else ""
                    print(f"    - {index_name}: {fields}{unique}")
            else:
                print(f"\n  📋 {collection_name}: Sin índices")
                
        except Exception as e:
            print(f"  ❌ Error al verificar {collection_name}: {str(e)}")


def check_mongodb_connection(db):
    """Verifica la conexión a MongoDB."""
    try:
        db.command('ping')
        return True, "Conexión exitosa a MongoDB"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description='Gestiona índices de MongoDB para el proyecto Hockey'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Elimina todos los índices (excepto _id) antes de recrearlos'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Solo verifica y muestra los índices existentes'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🏒 MONGODB INDEX MANAGER - Hockey Acción")
    print("=" * 60)
    
    with app.app_context():
        db = mongo.db
        
        # Verificar conexión
        connected, msg = check_mongodb_connection(db)
        if not connected:
            print(f"\n❌ {msg}")
            sys.exit(1)
        print(f"\n✅ {msg}")
        
        # Ejecutar según opciones
        if args.verify:
            verify_indexes(db)
        else:
            if args.reset:
                reset_indexes(db)
            
            print("\n📦 Creando índices...")
            created, skipped, errors = create_collection_indexes(db)
            
            # Resumen
            print("\n" + "=" * 60)
            print("📊 RESUMEN")
            print("=" * 60)
            print(f"✓ Índices creados: {created}")
            print(f"⏭️  Índices existentes: {skipped}")
            
            if errors:
                print(f"❌ Errores: {len(errors)}")
                for error in errors:
                    print(f"   - {error}")
                sys.exit(1)
            else:
                print(f"\n✅ Todos los índices están listos (Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
                sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario.")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
