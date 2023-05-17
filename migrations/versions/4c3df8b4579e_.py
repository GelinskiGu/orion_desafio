"""empty message

Revision ID: 4c3df8b4579e
Revises: dbb470b677e5
Create Date: 2023-05-17 09:44:18.877585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c3df8b4579e'
down_revision = 'dbb470b677e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(),
               type_=sa.LargeBinary(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.LargeBinary(),
               type_=sa.VARCHAR(),
               existing_nullable=False)

    # ### end Alembic commands ###
