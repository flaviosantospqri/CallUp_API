"""empty message

Revision ID: c9ae3bc6f997
Revises: 4812fc0f7116
Create Date: 2022-03-07 22:28:34.847144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c9ae3bc6f997"
down_revision = "4812fc0f7116"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "companies", "password_hash", existing_type=sa.VARCHAR(), nullable=True
    )
    op.create_unique_constraint(None, "companies", ["email"])
    op.alter_column(
        "providers",
        "password_hash",
        existing_type=sa.VARCHAR(length=511),
        nullable=True,
    )
    op.create_unique_constraint(None, "providers", ["cnpj"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "providers", type_="unique")
    op.alter_column(
        "providers",
        "password_hash",
        existing_type=sa.VARCHAR(length=511),
        nullable=False,
    )
    op.drop_constraint(None, "companies", type_="unique")
    op.alter_column(
        "companies", "password_hash", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###
