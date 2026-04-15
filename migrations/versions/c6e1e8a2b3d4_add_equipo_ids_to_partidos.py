"""add equipo ids to partidos

Revision ID: c6e1e8a2b3d4
Revises: bfef7fe7fe62
Create Date: 2025-10-18 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6e1e8a2b3d4'
down_revision = 'bfef7fe7fe62'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    # Resolver nombres reales de tablas respetando mayúsculas/minúsculas y esquema
    def all_table_names():
        names = []
        try:
            names.extend(insp.get_table_names())
        except Exception:
            pass
        try:
            names.extend(insp.get_table_names(schema='public'))
        except Exception:
            pass
        # Eliminar duplicados conservando orden
        seen = set()
        out = []
        for n in names:
            if n not in seen:
                out.append(n)
                seen.add(n)
        return out

    table_map = {n.lower(): n for n in all_table_names()}
    table_name = table_map.get('partidos')
    fk_table = table_map.get('equipos')

    if not table_name:
        # Si no existe la tabla, no hay nada que migrar en este paso
        return
    if not fk_table:
        # Si no existe Equipos aún, también salimos (evita romper upgrades parciales)
        return

    existing_cols = {c['name'] for c in insp.get_columns(table_name, schema='public')}
    existing_fks = {fk['name'] for fk in insp.get_foreign_keys(table_name, schema='public') if fk.get('name')}
    existing_idxs = {ix['name'] for ix in insp.get_indexes(table_name, schema='public')}

    # Agregar columnas opcionales para equipos específicos si no existen
    if 'equipo_local_id' not in existing_cols:
        op.add_column(table_name, sa.Column('equipo_local_id', sa.Integer(), nullable=True))
    if 'equipo_visitante_id' not in existing_cols:
        op.add_column(table_name, sa.Column('equipo_visitante_id', sa.Integer(), nullable=True))

    # Crear claves foráneas a Equipos.id si no existen
    if 'fk_partidos_equipo_local' not in existing_fks and 'equipo_local_id' in (existing_cols | {'equipo_local_id'}):
        op.create_foreign_key(
            'fk_partidos_equipo_local',
            table_name, fk_table,
            ['equipo_local_id'], ['id'],
            ondelete='SET NULL'
        )
    if 'fk_partidos_equipo_visitante' not in existing_fks and 'equipo_visitante_id' in (existing_cols | {'equipo_visitante_id'}):
        op.create_foreign_key(
            'fk_partidos_equipo_visitante',
            table_name, fk_table,
            ['equipo_visitante_id'], ['id'],
            ondelete='SET NULL'
        )

    # Índices opcionales para mejorar consultas si no existen
    if 'ix_partidos_equipo_local_id' not in existing_idxs:
        op.create_index('ix_partidos_equipo_local_id', table_name, ['equipo_local_id'])
    if 'ix_partidos_equipo_visitante_id' not in existing_idxs:
        op.create_index('ix_partidos_equipo_visitante_id', table_name, ['equipo_visitante_id'])


def downgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    table_map = {n.lower(): n for n in insp.get_table_names(schema='public')}
    table_name = table_map.get('partidos', 'Partidos')
    # Acciones de reversión con tolerancia a ausencia
    try:
        op.drop_index('ix_partidos_equipo_visitante_id', table_name=table_name)
    except Exception:
        pass
    try:
        op.drop_index('ix_partidos_equipo_local_id', table_name=table_name)
    except Exception:
        pass
    try:
        op.drop_constraint('fk_partidos_equipo_visitante', table_name, type_='foreignkey')
    except Exception:
        pass
    try:
        op.drop_constraint('fk_partidos_equipo_local', table_name, type_='foreignkey')
    except Exception:
        pass
    try:
        op.drop_column(table_name, 'equipo_visitante_id')
    except Exception:
        pass
    try:
        op.drop_column(table_name, 'equipo_local_id')
    except Exception:
        pass
