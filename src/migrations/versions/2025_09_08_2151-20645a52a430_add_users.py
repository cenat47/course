"""add_users

Revision ID: 20645a52a430
Revises: 611d10e119e5
Create Date: 2025-09-08 21:51:13.683103

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20645a52a430"
down_revision: Union[str, Sequence[str], None] = "611d10e119e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "Users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("Users")
