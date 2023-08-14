"""init migration

Revision ID: efac6954ee5f
Revises: 
Create Date: 2023-08-13 16:24:04.759839+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'efac6954ee5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'MODERATOR', 'ACCOUNTANT', 'WORKER', name='userrole'), nullable=False),
    sa.Column('bill', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='дата и время создания'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='дата и время последнего обновления'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='логическое удаление объекта'),
    sa.PrimaryKeyConstraint('id', name=op.f('PK_users')),
    sa.UniqueConstraint('bill', name=op.f('UQ_users_bill')),
    sa.UniqueConstraint('email', name=op.f('UQ_users_email')),
    sa.UniqueConstraint('password', name=op.f('UQ_users_password')),
    sa.UniqueConstraint('username', name=op.f('UQ_users_username')),
    schema='public'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users', schema='public')
    # ### end Alembic commands ###