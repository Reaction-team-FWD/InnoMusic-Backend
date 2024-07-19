"""Add images for users, songs and albums

Revision ID: 47626c630156
Revises: b49dd2a99737
Create Date: 2024-07-19 17:01:11.405719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "47626c630156"
down_revision: Union[str, None] = "b49dd2a99737"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("albums", sa.Column("cover", sa.LargeBinary(), nullable=True))
    op.add_column("songs", sa.Column("cover", sa.LargeBinary(), nullable=True))
    op.add_column("users", sa.Column("profile_picture", sa.LargeBinary(), nullable=True))
    op.alter_column("users", "name", existing_type=sa.VARCHAR(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users", "name", existing_type=sa.VARCHAR(), nullable=True)
    op.drop_column("users", "profile_picture")
    op.drop_column("songs", "cover")
    op.drop_column("albums", "cover")
    # ### end Alembic commands ###
