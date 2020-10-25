"""empty message

Revision ID: 75e3457dd6ae
Revises: 38d2f8d1951b
Create Date: 2020-10-25 15:54:22.734029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75e3457dd6ae'
down_revision = '38d2f8d1951b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_notes_created_at'), 'notes', ['created_at'], unique=False)
    op.create_index(op.f('ix_notes_due_date'), 'notes', ['due_date'], unique=False)
    op.create_foreign_key(None, 'notes', 'user', ['owner_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'notes', type_='foreignkey')
    op.drop_index(op.f('ix_notes_due_date'), table_name='notes')
    op.drop_index(op.f('ix_notes_created_at'), table_name='notes')
    # ### end Alembic commands ###
