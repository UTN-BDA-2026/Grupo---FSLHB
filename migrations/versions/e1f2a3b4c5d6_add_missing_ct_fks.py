"""add missing foreign keys for cuerpo_tecnico tables

Revision ID: e1f2a3b4c5d6
Revises: bb38acd6bd8d
Create Date: 2025-10-31 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1f2a3b4c5d6'
down_revision = 'bb38acd6bd8d'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    insp = sa.inspect(bind)

    def regclass_exists(qualified_name: str) -> bool:
        try:
            return bool(bind.execute(sa.text("SELECT to_regclass(:n) IS NOT NULL"), {"n": qualified_name}).scalar())
        except Exception:
            return False

    # cuerpo_tecnico: FK club_id -> "Clubes"(id)
    if regclass_exists('public.cuerpo_tecnico') and regclass_exists('public."Clubes"'):
        try:
            fks = {fk.get('name') for fk in insp.get_foreign_keys('cuerpo_tecnico', schema='public') if fk.get('name')}
        except Exception:
            fks = set()
        if 'fk_cuerpo_tecnico_club' not in fks:
            op.execute('ALTER TABLE public.cuerpo_tecnico ADD CONSTRAINT fk_cuerpo_tecnico_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id) ON DELETE CASCADE;')

    # cuerpo_tecnico_partido: FKs partido_id -> "Partidos"(id), club_id -> "Clubes"(id), cuerpo_tecnico_id -> cuerpo_tecnico(id)
    if regclass_exists('public.cuerpo_tecnico_partido'):
        try:
            fks_ctp = {fk.get('name') for fk in insp.get_foreign_keys('cuerpo_tecnico_partido', schema='public') if fk.get('name')}
        except Exception:
            fks_ctp = set()

        if regclass_exists('public."Partidos"') and 'fk_ct_partido_partido' not in fks_ctp:
            op.execute('ALTER TABLE public.cuerpo_tecnico_partido ADD CONSTRAINT fk_ct_partido_partido FOREIGN KEY (partido_id) REFERENCES public."Partidos"(id) ON DELETE CASCADE;')
        if regclass_exists('public."Clubes"') and 'fk_ct_partido_club' not in fks_ctp:
            op.execute('ALTER TABLE public.cuerpo_tecnico_partido ADD CONSTRAINT fk_ct_partido_club FOREIGN KEY (club_id) REFERENCES public."Clubes"(id) ON DELETE CASCADE;')
        if regclass_exists('public.cuerpo_tecnico') and 'fk_ct_partido_ct' not in fks_ctp:
            op.execute('ALTER TABLE public.cuerpo_tecnico_partido ADD CONSTRAINT fk_ct_partido_ct FOREIGN KEY (cuerpo_tecnico_id) REFERENCES public.cuerpo_tecnico(id) ON DELETE CASCADE;')


def downgrade():
    # Drop constraints if they exist (tolerant)
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico_partido DROP CONSTRAINT IF EXISTS fk_ct_partido_ct;')
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico_partido DROP CONSTRAINT IF EXISTS fk_ct_partido_club;')
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico_partido DROP CONSTRAINT IF EXISTS fk_ct_partido_partido;')
    op.execute('ALTER TABLE IF EXISTS public.cuerpo_tecnico DROP CONSTRAINT IF EXISTS fk_cuerpo_tecnico_club;')
