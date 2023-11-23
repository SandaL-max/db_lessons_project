"""GIN index test1

Revision ID: 0f2730f54bea
Revises: 3614cc5f29ff
Create Date: 2023-11-16 14:44:55.134258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from models.worker import Worker


# revision identifiers, used by Alembic.
revision: str = "0f2730f54bea"
down_revision: Union[str, None] = "3614cc5f29ff"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        Worker.index.name,
        Worker.index.table.name,
        Worker.index.expressions,
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"columns": "gin_trgm_ops"},
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        "workers_full_name_post_idx",
        table_name="workers",
        postgresql_using="gin",
        postgresql_ops={"columns": "gin_trgm_ops"},
    )
    # ### end Alembic commands ###