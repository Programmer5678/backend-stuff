"""create table ass

Revision ID: 47ca7edae369
Revises: 651b997fcf9f
Create Date: 2025-04-10 20:59:09.473560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47ca7edae369'
down_revision: Union[str, None] = '651b997fcf9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create table ass2 (id int primary key);")


def downgrade() -> None:
    op.execute("drop table ass2;")
