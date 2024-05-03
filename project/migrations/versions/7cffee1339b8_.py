"""empty message

Revision ID: 7cffee1339b8
Revises: 93bd9f255724
Create Date: 2024-03-27 11:59:12.849593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7cffee1339b8'
down_revision = '93bd9f255724'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('borrow_books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('issue_date', sa.Date(), nullable=True),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('issued_by', sa.Integer(), nullable=True),
    sa.Column('fine', sa.Integer(), nullable=True),
    sa.Column('fine_days', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('expected_return_date', sa.Date(), nullable=True),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('books_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['books_id'], ['books.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('borrow_books')
    # ### end Alembic commands ###