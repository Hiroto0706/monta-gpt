"""create_messages_table

Revision ID: c50aad860463
Revises: c8e3508b6c3a
Create Date: 2024-09-28 18:26:33.279125

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = "c50aad860463"
down_revision: Union[str, None] = "c8e3508b6c3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "session_id",
            sa.Integer(),
            sa.ForeignKey("chat_sessions.id"),
            nullable=False,
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "timestamp", sa.TIMESTAMP(), server_default=func.now(), nullable=False
        ),
        sa.Column("is_user", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(), server_default=func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_id"), "messages", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_messages_id"), table_name="messages")
    op.drop_table("messages")
