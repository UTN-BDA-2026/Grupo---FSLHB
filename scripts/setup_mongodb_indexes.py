"""
Inicializa y verifica índices de MongoDB para optimizar búsquedas.

Este script debe ejecutarse una sola vez después de crear la base de datos.

Uso:
    python scripts/setup_mongodb_indexes.py              # Crear índices
    python scripts/setup_mongodb_indexes.py --reset      # Resetear todos los índices
    python scripts/setup_mongodb_indexes.py --verify     # Solo verificar índices existentes

Índices creados:
    - usuarios: username (único), is_admin, is_operador, club_id
    - clubes: nombre (único)
    - equipos: nombre (único), club_id, categoria, club_id+categoria (compuesto)
    - partidos: fecha, torneo_id, equipo_local_id, equipo_visitante_id,
                torneo+categoria+fecha_numero (compuesto), estado,
                club_local_id+club_visitante_id (compuesto)
    - incidencias: partido_id+tipo (compuesto), partido_id+created_at (compuesto),
                   jugadora_id+tipo (compuesto), partido_id+club_id (compuesto)
    - noticias: fecha, titulo
    - torneo: nombre (único)
    - jugadora: nombre, club_id
    - arbitros: apellido+nombre (compuesto), dni (único, sparse)
    - arbitro_partido: partido_id, partido_id+club_id (único)
    - cuerpo_tecnico: club_id+rol (compuesto), dni (sparse)
    - cuerpo_tecnico_partido: partido_id, partido_id+club_id+rol (único)
    - precarga_jugadoras: partido_id+club_id (compuesto),
                          partido_id+club_id+jugadora_id (único)
    - notas_partido: partido_id (único)
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


# Lista centralizada de colecciones gestionadas por este script

MANAGED_COLLECTIONS = [
    'usuarios', 'clubes', 'equipos', 'partidos', 'incidencias',
    'noticias', 'torneos', 'jugadora',
    'arbitros', 'arbitro_partido',
    'cuerpo_tecnico', 'cuerpo_tecnico_partido',
    'precarga_jugadoras', 'notas_partido',
]


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

        # ── Usuarios ──
        ('usuarios', [
            (([('username', 1)], {'unique': True}), 'Username único'),
            (([('is_admin', 1)], {}), 'Búsqueda de admins'),
            (([('is_operador', 1)], {}), 'Búsqueda de operadores'),
            (([('club_id', 1)], {}), 'Búsqueda por club'),
        ]),

        # ── Clubes ──
        ('clubes', [
            (([('nombre', 1)], {'unique': True}), 'Nombre único'),
        ]),

        # ── Equipos ──
        ('equipos', [
            (([('nombre', 1)], {'unique': True}), 'Nombre único'),
            (([('club_id', 1)], {}), 'Búsqueda por club'),
            (([('categoria', 1)], {}), 'Filtro por categoría'),
            (([('club_id', 1), ('categoria', 1)], {}), 'Equipos por club y categoría'),
        ]),

        # ── Partidos ──
        ('partidos', [
            (([('fecha', -1)], {}), 'Ordena por fecha (reciente primero)'),
            (([('torneo_id', 1)], {}), 'Búsqueda por torneo'),
            (([('equipo_local_id', 1)], {}), 'Búsqueda por equipo local'),
            (([('equipo_visitante_id', 1)], {}), 'Búsqueda por equipo visitante'),
            (([('torneo', 1), ('categoria', 1), ('fecha_numero', 1)], {}),
             'Búsqueda ranking (torneo + categoría + fecha)'),
            (([('estado', 1)], {}), 'Filtro por estado'),
            (([('club_local_id', 1), ('club_visitante_id', 1)], {}),
             'Búsqueda por clubes participantes'),
        ]),

        # ── Incidencias ──
        ('incidencias', [
            (([('partido_id', 1)], {}), 'Búsqueda por partido'),
            (([('jugadora_id', 1)], {}), 'Búsqueda por jugadora'),
            (([('tipo_incidencia', 1)], {}), 'Búsqueda por tipo de incidencia'),
            (([('partido_id', 1), ('tipo', 1)], {}),
             'Búsqueda por partido y tipo (goles/tarjetas)'),
            (([('partido_id', 1), ('created_at', 1)], {}),
             'Listado por partido ordenado por fecha'),
            (([('jugadora_id', 1), ('tipo', 1)], {}),
             'Tarjetas/goles por jugadora'),
            (([('partido_id', 1), ('club_id', 1)], {}),
             'Incidencias por partido y club'),
        ]),

        # ── Noticias ──
        ('noticias', [
            (([('fecha', -1)], {}), 'Ordena por fecha (reciente primero)'),
            (([('titulo', 1)], {}), 'Búsqueda por título'),
        ]),

        # ── Torneos ──
        ('torneos', [
            (([('nombre', 1)], {'unique': True}), 'Nombre único'),
        ]),

        # ── Jugadora ──
        ('jugadora', [
            (([('nombre', 1)], {}), 'Búsqueda por nombre'),
            (([('club_id', 1)], {}), 'Búsqueda por club'),
        ]),

        # ── Árbitros ──
        ('arbitros', [
            (([('apellido', 1), ('nombre', 1)], {}),
             'Ordenamiento por apellido/nombre'),
            (([('dni', 1)], {'unique': True, 'sparse': True}),
             'DNI único (sparse)'),
        ]),

        # ── Árbitro ↔ Partido ──
        ('arbitro_partido', [
            (([('partido_id', 1)], {}), 'Búsqueda por partido'),
            (([('partido_id', 1), ('club_id', 1)], {'unique': True}),
             'Partido + club único'),
        ]),

        # ── Cuerpo Técnico ──
        ('cuerpo_tecnico', [
            (([('club_id', 1), ('rol', 1)], {}),
             'Búsqueda por club y rol'),
            (([('dni', 1)], {'sparse': True}),
             'Búsqueda por DNI (sparse)'),
        ]),

        # ── Cuerpo Técnico ↔ Partido ──
        ('cuerpo_tecnico_partido', [
            (([('partido_id', 1)], {}), 'Búsqueda por partido'),
            (([('partido_id', 1), ('club_id', 1), ('rol', 1)], {'unique': True}),
             'Partido + club + rol único'),
        ]),

        # ── Precarga de Jugadoras ──
        ('precarga_jugadoras', [
            (([('partido_id', 1), ('club_id', 1)], {}),
             'Búsqueda por partido y club'),
            (([('partido_id', 1), ('club_id', 1), ('jugadora_id', 1)], {'unique': True}),
             'Evita duplicados de jugadora por partido/club'),
        ]),

        # ── Notas de Partido ──
        ('notas_partido', [
            (([('partido_id', 1)], {'unique': True}),
             'Una nota por partido'),
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
    
    for collection_name in MANAGED_COLLECTIONS:
        try:
            collection = db[collection_name]
            # drop_index() borra un índice por nombre, drop_indexes() borra todos excepto _id
            collection.drop_indexes()
            print(f"  ✓ Índices eliminados en {collection_name}")
        except Exception as e:
            print(f"  ⚠️  {collection_name}: {str(e)}")


def verify_indexes(db):
    """Verifica y muestra los índices existentes."""
    print("\n🔍 Índices actuales en MongoDB:")
    
    total_indexes = 0

    for collection_name in MANAGED_COLLECTIONS:
        try:
            collection = db[collection_name]
            indexes = get_existing_indexes(collection)
            
            if indexes:
                print(f"\n  📋 {collection_name}:")
                for index_name, index_info in indexes.items():
                    fields = ', '.join([f"{k} ({v})" for k, v in index_info['key']])
                    unique = " (único)" if index_info.get('unique', False) else ""
                    sparse = " (sparse)" if index_info.get('sparse', False) else ""
                    print(f"    - {index_name}: {fields}{unique}{sparse}")
                    total_indexes += 1
            else:
                print(f"\n  📋 {collection_name}: Sin índices")
                
        except Exception as e:
            print(f"  ❌ Error al verificar {collection_name}: {str(e)}")

    print(f"\n  📊 Total de índices: {total_indexes}")


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
            print(f"  Colecciones gestionadas: {len(MANAGED_COLLECTIONS)}")
            print(f"  ✓ Índices creados: {created}")
            print(f"  ⏭️  Índices existentes: {skipped}")
            
            if errors:
                print(f"  ❌ Errores: {len(errors)}")
                for error in errors:
                    print(f"     - {error}")
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
