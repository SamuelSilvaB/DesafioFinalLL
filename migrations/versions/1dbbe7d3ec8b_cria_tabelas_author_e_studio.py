"""cria tabelas author e studio

Revision ID: 1dbbe7d3ec8b
Revises: cb16a4621db2
Create Date: 2026-10-12 16:45:21.583182

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dbbe7d3ec8b'
down_revision: Union[str, Sequence[str], None] = 'cb16a4621db2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'author',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'studio',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )

    with op.batch_alter_table('anime', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('studio_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_anime_author', 'author', ['author_id'], ['id'])
        batch_op.create_foreign_key('fk_anime_studio', 'studio', ['studio_id'], ['id'])

def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('anime', schema=None) as batch_op:
        batch_op.drop_constraint('fk_anime_author', type_='foreignkey')
        batch_op.drop_constraint('fk_anime_studio', type_='foreignkey')
        batch_op.drop_column('studio_id')
        batch_op.drop_column('author_id')

    op.drop_table('studio')
    op.drop_table('author')