"""create_chat_sessions_table

Revision ID: c8e3508b6c3a
Revises: 43f5b322edc6
Create Date: 2024-09-28 18:10:16.758654

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = "c8e3508b6c3a"
down_revision: Union[str, None] = "43f5b322edc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "chat_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("start_time", sa.TIMESTAMP()),
        sa.Column("end_time", sa.TIMESTAMP()),
        sa.Column("summary", sa.Text()),
        sa.Column(
            "created_at", sa.TIMESTAMP(), server_default=func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_chat_sessions_id"), table_name="chat_sessions")
    op.drop_table("chat_sessions")
