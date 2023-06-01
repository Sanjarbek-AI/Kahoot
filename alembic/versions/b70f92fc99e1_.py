"""empty message

Revision ID: b70f92fc99e1
Revises: 1c6218269347
Create Date: 2023-05-31 19:53:16.179240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70f92fc99e1'
down_revision = '1c6218269347'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activegames',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generated_code', sa.Integer(), nullable=True),
    sa.Column('total_users', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("(now() AT TIME ZONE 'Asia/Tashkent')"), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("(now() AT TIME ZONE 'Asia/Tashkent')"), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['games.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_activegames_generated_code'), 'activegames', ['generated_code'], unique=True)
    op.create_index(op.f('ix_activegames_id'), 'activegames', ['id'], unique=False)
    op.create_table('activegamers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('generated_code', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('image', sa.String(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("(now() AT TIME ZONE 'Asia/Tashkent')"), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text("(now() AT TIME ZONE 'Asia/Tashkent')"), nullable=False),
    sa.ForeignKeyConstraint(['generated_code'], ['activegames.generated_code'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_activegamers_id'), 'activegamers', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_activegamers_id'), table_name='activegamers')
    op.drop_table('activegamers')
    op.drop_index(op.f('ix_activegames_id'), table_name='activegames')
    op.drop_index(op.f('ix_activegames_generated_code'), table_name='activegames')
    op.drop_table('activegames')
    # ### end Alembic commands ###
