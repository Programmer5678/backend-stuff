"""add row to yummy

Revision ID: 0b7a9908c766
Revises: 
Create Date: 2025-04-10 21:21:53.441115

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0b7a9908c766'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("insert into yummy(s) values('stringy')")


def downgrade() -> None:
    op.execute("delete from yummy where id = (select * from (select id from yummy order by id desc limit 1)tableTmp )")
