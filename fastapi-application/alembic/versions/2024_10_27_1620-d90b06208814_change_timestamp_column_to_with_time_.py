"""Change timestamp column to WITH TIME ZONE

Revision ID: d90b06208814
Revises: 7e486c07628b
Create Date: 2024-10-27 16:20:55.175188

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd90b06208814'
down_revision: str | None = '7e486c07628b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade():
    op.alter_column('prices', 'timestamp', type_=sa.DateTime(timezone=True), existing_type=sa.DateTime(timezone=False))


def downgrade():
    op.alter_column('prices', 'timestamp', type_=sa.DateTime(timezone=False), existing_type=sa.DateTime(timezone=True))
