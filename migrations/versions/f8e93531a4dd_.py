"""empty message
Revision ID: f8e93531a4dd
Revises: 
Create Date: 2022-03-04 21:42:25.624078
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f8e93531a4dd"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "subcategories",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "companies",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("cnpj", sa.String(), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "sectors",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=225), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "employees",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("company_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("sector_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("phone", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
        ),
        sa.ForeignKeyConstraint(
            ["sector_id"],
            ["sectors.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "calls",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("description", sa.String(length=225), nullable=True),
        sa.Column("open", sa.Boolean(), nullable=True),
        sa.Column("scheduling", sa.Date(), nullable=True),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("subcategory_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"],
        ),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
        ),
        sa.ForeignKeyConstraint(
            ["subcategory_id"],
            ["subcategories.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "providers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=127), nullable=False),
        sa.Column("cnpj", sa.String(length=511), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("about", sa.String(length=255), nullable=True),
        sa.Column("password_hash", sa.String(length=511), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "proposals",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("price", sa.Float(precision=2), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=False),
        sa.Column("call_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["call_id"],
            ["calls.id"],
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["providers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "providers_customers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("provider_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("employee_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["employee_id"],
            ["employees.id"],
        ),
        sa.ForeignKeyConstraint(
            ["provider_id"],
            ["providers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "calls",
        sa.Column("selected_proposal_id", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_foreign_key(
        "fk_call_selected_proposal_id", "calls", "proposals", ["selected_proposal_id"], ["id"]
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("providers_customers")
    op.drop_table("employees")
    op.drop_table("subcategories")
    op.drop_table("sectors")
    op.drop_table("providers")
    op.drop_table("proposals")
    op.drop_table("companies")
    op.drop_table("categories")
    op.drop_table("calls")
    # ### end Alembic commands ###
