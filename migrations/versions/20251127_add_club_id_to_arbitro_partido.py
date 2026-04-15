"""add club_id to arbitro_partido

Revision ID: add_club_id_arbitro_partido
Revises: e1f2a3b4c5d6
Create Date: 2025-11-27 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_club_id_arbitro_partido'
down_revision = '8f9bfd237692'
branch_labels = None
depends_on = None


def upgrade():
    # Add column club_id (nullable for backfill)
    with op.batch_alter_table('arbitro_partido') as batch_op:
        batch_op.add_column(sa.Column('club_id', sa.Integer(), nullable=True))
        # Drop old unique if exists and add new unique on (partido_id, club_id)
        try:
            batch_op.drop_constraint('uq_arbitro_partido_arbitro', type_='unique')
        except Exception:
            pass
        batch_op.create_unique_constraint('uq_arbitro_partido_equipo', ['partido_id', 'club_id'])
    # Add FK to "Clubes"(id) if tables exist
    try:
        op.create_foreign_key('fk_arbitro_partido_club', 'arbitro_partido', 'Clubes', ['club_id'], ['id'], source_schema='public', referent_schema='public', ondelete='CASCADE')
    except Exception:
        # tolerante si ya existe
        pass


def downgrade():
    with op.batch_alter_table('arbitro_partido') as batch_op:
        try:
            batch_op.drop_constraint('uq_arbitro_partido_equipo', type_='unique')
        except Exception:
            pass
        try:
            batch_op.drop_constraint('fk_arbitro_partido_club', type_='foreignkey')
        except Exception:
            pass
        batch_op.drop_column('club_id')
        batch_op.create_unique_constraint('uq_arbitro_partido_arbitro', ['partido_id', 'arbitro_id'])
