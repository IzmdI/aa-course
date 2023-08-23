"""init billing migration

Revision ID: d04faab85ce0
Revises: 
Create Date: 2023-08-21 12:21:44.346275+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd04faab85ce0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billing_cycle',
    sa.Column('public_id', sa.Uuid(), nullable=False),
    sa.Column('total_income', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='дата и время создания'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='дата и время последнего обновления'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='логическое удаление объекта'),
    sa.PrimaryKeyConstraint('id', name=op.f('PK_billing_cycle')),
    sa.UniqueConstraint('public_id', name=op.f('UQ_billing_cycle_public_id')),
    schema='billing'
    )
    op.create_index(op.f('IX_billing_billing_cycle_id'), 'billing_cycle', ['id'], unique=False, schema='billing')
    op.create_table('users',
    sa.Column('public_id', sa.Uuid(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('role', sa.Enum('ADMIN', 'MODERATOR', 'ACCOUNTANT', 'WORKER', name='userrole', schema='billing'), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('balance', sa.BigInteger(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='дата и время создания'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='дата и время последнего обновления'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='логическое удаление объекта'),
    sa.PrimaryKeyConstraint('id', name=op.f('PK_users')),
    sa.UniqueConstraint('email', name=op.f('UQ_users_email')),
    sa.UniqueConstraint('public_id', name=op.f('UQ_users_public_id')),
    sa.UniqueConstraint('username', name=op.f('UQ_users_username')),
    schema='billing'
    )
    op.create_index(op.f('IX_billing_users_id'), 'users', ['id'], unique=False, schema='billing')
    op.create_table('billing_transactions',
    sa.Column('public_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('credit', sa.BigInteger(), nullable=False),
    sa.Column('debit', sa.BigInteger(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('type', sa.Enum('TASK', 'PAYMENT', name='transactiontype', schema='billing'), nullable=False),
    sa.Column('billing_cycle_id', sa.Uuid(), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='дата и время создания'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='дата и время последнего обновления'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='логическое удаление объекта'),
    sa.ForeignKeyConstraint(['billing_cycle_id'], ['billing.billing_cycle.public_id'], name=op.f('FK_billing_transactions_billing_cycle_id_billing_cycle')),
    sa.PrimaryKeyConstraint('id', name=op.f('PK_billing_transactions')),
    sa.UniqueConstraint('public_id', name=op.f('UQ_billing_transactions_public_id')),
    schema='billing'
    )
    op.create_index(op.f('IX_billing_billing_transactions_id'), 'billing_transactions', ['id'], unique=False, schema='billing')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('IX_billing_billing_transactions_id'), table_name='billing_transactions', schema='billing')
    op.drop_table('billing_transactions', schema='billing')
    op.drop_index(op.f('IX_billing_users_id'), table_name='users', schema='billing')
    op.drop_table('users', schema='billing')
    op.drop_index(op.f('IX_billing_billing_cycle_id'), table_name='billing_cycle', schema='billing')
    op.drop_table('billing_cycle', schema='billing')
    # ### end Alembic commands ###