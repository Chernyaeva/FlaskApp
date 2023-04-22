"""add articles-tags association table

Revision ID: 8f3bc40a6d57
Revises: e7772b13628d
Create Date: 2023-04-22 21:05:27.108989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f3bc40a6d57'
down_revision = 'e7772b13628d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_tag_association',
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], name=op.f('fk_article_tag_association_article_id_article')),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], name=op.f('fk_article_tag_association_tag_id_tag'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article_tag_association')
    # ### end Alembic commands ###
