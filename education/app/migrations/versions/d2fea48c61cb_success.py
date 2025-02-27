"""Success

Revision ID: d2fea48c61cb
Revises: 
Create Date: 2024-06-25 11:40:58.723229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2fea48c61cb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('block', sa.String(), nullable=False),
    sa.Column('theme', sa.String(), nullable=False),
    sa.Column('lesson', sa.String(), nullable=False),
    sa.Column('theory_source', sa.String(), nullable=False),
    sa.Column('practice_source', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_templates', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('organization', sa.String(), nullable=True),
    sa.Column('tin', sa.String(), nullable=False),
    sa.Column('web_site', sa.String(), nullable=True),
    sa.Column('business', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('post', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('blocks')
    # ### end Alembic commands ###
