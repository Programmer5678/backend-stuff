"""alternative: create table boobs

Revision ID: 9ee5037f44fc
Revises: 81e92c043c6a
Create Date: 2025-04-10 21:10:08.338577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ee5037f44fc'
down_revision: Union[str, None] = '651b997fcf9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("create table boobs (id int primary key)")

def downgrade() -> None:
    op.execute("drop table boobs")
