"""Cambio division a categoria y elimina rama en Jugadora

Revision ID: bfef7fe7fe62
Revises: 
Create Date: 2025-10-09 20:35:59.409663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfef7fe7fe62'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Esta migración intentaba achicar la columna password a VARCHAR(128),
    # pero puede fallar si hay hashes más largos. No hacemos cambios aquí.
    pass


def downgrade():
    pass
