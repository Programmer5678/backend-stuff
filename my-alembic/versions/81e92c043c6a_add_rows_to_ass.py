"""add rows to ass

Revision ID: 81e92c043c6a
Revises: 47ca7edae369
Create Date: 2025-04-10 21:05:34.329050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '81e92c043c6a'
down_revision: Union[str, None] = '47ca7edae369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("insert into ass2 values(100)")


def downgrade() -> None:
    op.execute("delete from ass2 where id=100")
