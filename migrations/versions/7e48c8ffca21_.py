"""empty message

Revision ID: 7e48c8ffca21
Revises: 415ce01cbd05
Create Date: 2022-03-10 01:04:03.399219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7e48c8ffca21'
down_revision = '415ce01cbd05'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calls', sa.Column('selected_proposal_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.alter_column('calls', 'category_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('calls', 'subcategory_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('calls', 'employee_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.drop_constraint('fk_call_selected_proposal', 'calls', type_='foreignkey')
    op.create_foreign_key(None, 'calls', 'proposals', ['selected_proposal_id'], ['id'])
    op.drop_column('calls', 'selected_proposal')
    op.add_column('companies', sa.Column('type', sa.String(), nullable=True))
    op.add_column('employees', sa.Column('type', sa.String(), nullable=True))
    op.alter_column('employees', 'company_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.alter_column('employees', 'sector_id',
               existing_type=postgresql.UUID(),
               nullable=True)
    op.add_column('providers', sa.Column('type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('providers', 'type')
    op.alter_column('employees', 'sector_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('employees', 'company_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('employees', 'type')
    op.drop_column('companies', 'type')
    op.add_column('calls', sa.Column('selected_proposal', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'calls', type_='foreignkey')
    op.create_foreign_key('fk_call_selected_proposal', 'calls', 'proposals', ['selected_proposal'], ['id'])
    op.alter_column('calls', 'employee_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('calls', 'subcategory_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.alter_column('calls', 'category_id',
               existing_type=postgresql.UUID(),
               nullable=False)
    op.drop_column('calls', 'selected_proposal_id')
    # ### end Alembic commands ###