"""Added object relational methods

Revision ID: 040df501ec6e
Revises: 9f65c5b09d66
Create Date: 2023-09-03 16:27:28.511524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '040df501ec6e'
down_revision: Union[str, None] = '9f65c5b09d66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
