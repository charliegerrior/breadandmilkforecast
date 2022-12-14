"""empty message

Revision ID: 57d979d880ca
Revises: 
Create Date: 2018-10-30 15:10:14.272623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57d979d880ca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('forecast',
    sa.Column('region', sa.String(length=5), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('bread_mean', sa.Integer(), nullable=True),
    sa.Column('bread_percent', sa.Integer(), nullable=True),
    sa.Column('bread_distance', sa.Integer(), nullable=True),
    sa.Column('eggs_mean', sa.Integer(), nullable=True),
    sa.Column('eggs_percent', sa.Integer(), nullable=True),
    sa.Column('eggs_distance', sa.Integer(), nullable=True),
    sa.Column('milk_mean', sa.Integer(), nullable=True),
    sa.Column('milk_percent', sa.Integer(), nullable=True),
    sa.Column('milk_distance', sa.Integer(), nullable=True),
    sa.Column('tp_mean', sa.Integer(), nullable=True),
    sa.Column('tp_percent', sa.Integer(), nullable=True),
    sa.Column('tp_distance', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('region')
    )
    op.create_index(op.f('ix_forecast_timestamp'), 'forecast', ['timestamp'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('number', sa.String(length=64), nullable=True),
    sa.Column('region', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=False)
    op.create_index(op.f('ix_user_number'), 'user', ['number'], unique=True)
    op.create_index(op.f('ix_user_region'), 'user', ['region'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_region'), table_name='user')
    op.drop_index(op.f('ix_user_number'), table_name='user')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_forecast_timestamp'), table_name='forecast')
    op.drop_table('forecast')
    # ### end Alembic commands ###
