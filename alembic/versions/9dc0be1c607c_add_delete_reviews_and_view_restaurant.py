"""add,delete reviews and view restaurant

Revision ID: 9dc0be1c607c
Revises: 7ea98261cafb
Create Date: 2023-09-03 20:11:13.239353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9dc0be1c607c'
down_revision: Union[str, None] = '7ea98261cafb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
