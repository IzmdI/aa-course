"""init tasks migration

Revision ID: 245358b60f38
Revises: 
Create Date: 2023-08-20 16:13:25.850421+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '245358b60f38'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('title', sa.String(length=320), nullable=False),
    sa.Column('public_id', sa.Uuid(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('fee', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.Column('assignee_id', sa.Uuid(), nullable=False),
    sa.Column('status', sa.Enum('NEW', 'ASSIGNED', 'DONE', name='taskstatus', schema='tasks'), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='дата и время создания'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='дата и время последнего обновления'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='логическое удаление объекта'),
    sa.PrimaryKeyConstraint('id', name=op.f('PK_tasks')),
    sa.UniqueConstraint('public_id', name=op.f('UQ_tasks_public_id')),
    schema='tasks'
    )
    op.create_index(op.f('IX_tasks_tasks_id'), 'tasks', ['id'], unique=False, schema='tasks')
    op.create_table('users',
    sa.Column('public_id', sa.Uuid(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=True),
    sa.Column('role', sa.Enum('ADMIN', 'MODERATOR', 'ACCOUNTANT', 'WORKER', name='userrole', schema='tasks'), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False, comment='Идентификатор'),
    sa.Column('created_at', sa.DateTime(), nullable=False, comment='дата и время создания'),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False, comment='дата и время последнего обновления'),
    sa.Column('is_active', sa.Boolean(), nullable=False, comment='логическое удаление объекта'),
    sa.PrimaryKeyConstraint('id', name=op.f('PK_users')),
    sa.UniqueConstraint('email', name=op.f('UQ_users_email')),
    sa.UniqueConstraint('public_id', name=op.f('UQ_users_public_id')),
    sa.UniqueConstraint('username', name=op.f('UQ_users_username')),
    schema='tasks'
    )
    op.create_index(op.f('IX_tasks_users_id'), 'users', ['id'], unique=False, schema='tasks')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('IX_tasks_users_id'), table_name='users', schema='tasks')
    op.drop_table('users', schema='tasks')
    op.drop_index(op.f('IX_tasks_tasks_id'), table_name='tasks', schema='tasks')
    op.drop_table('tasks', schema='tasks')
    # ### end Alembic commands ###
