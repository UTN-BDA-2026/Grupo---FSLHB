"""add cuerpo tecnico tables

Revision ID: d9a1f2b3c4e5
Revises: c6e1e8a2b3d4
Create Date: 2025-10-20 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9a1f2b3c4e5'
down_revision = 'c6e1e8a2b3d4'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)
    
    # Helper: check if a given regclass exists (e.g., public."Clubes")
    def regclass_exists(qualified_name: str) -> bool:
        try:
            return bool(bind.execute(sa.text("SELECT to_regclass(:n) IS NOT NULL"), {"n": qualified_name}).scalar())
        except Exception:
            return False

    # Tabla de miembros del cuerpo técnico por club (si no existe)
    if 'cuerpo_tecnico' not in insp.get_table_names():
        op.create_table(
            'cuerpo_tecnico',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            # FK se agrega por SQL crudo más abajo para manejar correctamente mayúsculas de "Clubes"
            sa.Column('club_id', sa.Integer(), nullable=False),
            sa.Column('nombre', sa.String(length=80), nullable=False),
            sa.Column('apellido', sa.String(length=80), nullable=False),
            sa.Column('dni', sa.String(length=20), nullable=False),
            sa.Column('rol', sa.String(length=20), nullable=False),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        )
        op.create_index('ix_cuerpo_tecnico_club_id', 'cuerpo_tecnico', ['club_id'])

        # Agrega FK a "Clubes" (si la tabla existe) respetando mayúsculas/minúsculas
        fks = {fk.get('name') for fk in insp.get_foreign_keys('cuerpo_tecnico') if fk.get('name')}
        if 'fk_cuerpo_tecnico_club' not in fks and regclass_exists('public."Clubes"'):
            op.execute('ALTER TABLE public.cuerpo_tecnico ADD CONSTRAINT fk_cuerpo_tecnico_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id) ON DELETE CASCADE;')

    # Selección de cuerpo técnico por partido y club (si no existe)
    if 'cuerpo_tecnico_partido' not in insp.get_table_names():
        op.create_table(
            'cuerpo_tecnico_partido',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            # FKs se agregan por SQL crudo más abajo
            sa.Column('partido_id', sa.Integer(), nullable=False),
            sa.Column('club_id', sa.Integer(), nullable=False),
            sa.Column('rol', sa.String(length=32), nullable=False),
            sa.Column('cuerpo_tecnico_id', sa.Integer(), nullable=False),
        )
        op.create_unique_constraint('uq_ct_partido_club_rol', 'cuerpo_tecnico_partido', ['partido_id', 'club_id', 'rol'])
        op.create_index('ix_ct_partido_partido_id', 'cuerpo_tecnico_partido', ['partido_id'])
        op.create_index('ix_ct_partido_club_id', 'cuerpo_tecnico_partido', ['club_id'])

        # Agregar FKs con nombres explícitos (soporta "Partidos"/"Clubes")
        fks_ctp = {fk.get('name') for fk in insp.get_foreign_keys('cuerpo_tecnico_partido') if fk.get('name')}
        if 'fk_ct_partido_partido' not in fks_ctp and regclass_exists('public."Partidos"'):
            op.execute('ALTER TABLE public.cuerpo_tecnico_partido ADD CONSTRAINT fk_ct_partido_partido FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id) ON DELETE CASCADE;')
        if 'fk_ct_partido_club' not in fks_ctp and regclass_exists('public."Clubes"'):
            op.execute('ALTER TABLE public.cuerpo_tecnico_partido ADD CONSTRAINT fk_ct_partido_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id) ON DELETE CASCADE;')
        if 'fk_ct_partido_ct' not in fks_ctp:
            op.execute('ALTER TABLE public.cuerpo_tecnico_partido ADD CONSTRAINT fk_ct_partido_ct FOREIGN KEY (cuerpo_tecnico_id) REFERENCES public.cuerpo_tecnico(id) ON DELETE CASCADE;')


def downgrade():
    # Elimina FKs si existen y luego índices/tablas
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico_partido DROP CONSTRAINT IF EXISTS fk_ct_partido_ct;')
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico_partido DROP CONSTRAINT IF EXISTS fk_ct_partido_club;')
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico_partido DROP CONSTRAINT IF EXISTS fk_ct_partido_partido;')

    op.drop_index('ix_ct_partido_club_id', table_name='cuerpo_tecnico_partido')
    op.drop_index('ix_ct_partido_partido_id', table_name='cuerpo_tecnico_partido')
    op.drop_constraint('uq_ct_partido_club_rol', 'cuerpo_tecnico_partido', type_='unique')
    op.drop_table('cuerpo_tecnico_partido')

    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico DROP CONSTRAINT IF EXISTS fk_cuerpo_tecnico_club;')
    op.drop_index('ix_cuerpo_tecnico_club_id', table_name='cuerpo_tecnico')
    op.drop_table('cuerpo_tecnico')
