"""add last_accessed_at column

Revision ID: 3c9ee24ecefd
Revises: 
Create Date: 2024-03-21 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c9ee24ecefd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite doesn't support ALTER TABLE for adding columns with constraints
    # So we'll create a new table with the desired schema
    op.create_table(
        'matchmaking_results_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bride_name', sa.String(length=100), nullable=False),
        sa.Column('bride_dob', sa.Date(), nullable=False),
        sa.Column('bride_tob', sa.Time(), nullable=False),
        sa.Column('bride_place_id', sa.Integer(), nullable=False),
        sa.Column('groom_name', sa.String(length=100), nullable=False),
        sa.Column('groom_dob', sa.Date(), nullable=False),
        sa.Column('groom_tob', sa.Time(), nullable=False),
        sa.Column('groom_place_id', sa.Integer(), nullable=False),
        sa.Column('compatibility_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('compatibility', sa.String(length=50), nullable=False),
        sa.Column('remarks', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('last_accessed_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['bride_place_id'], ['places.id'], ),
        sa.ForeignKeyConstraint(['groom_place_id'], ['places.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data from old table to new table
    op.execute('''
        INSERT INTO matchmaking_results_new (
            id, bride_name, bride_dob, bride_tob, bride_place_id,
            groom_name, groom_dob, groom_tob, groom_place_id,
            compatibility_score, compatibility, remarks, created_at
        )
        SELECT 
            id, bride_name, bride_dob, bride_tob, bride_place_id,
            groom_name, groom_dob, groom_tob, groom_place_id,
            compatibility_score, compatibility, remarks, created_at
        FROM matchmaking_results
    ''')

    # Drop old table and rename new table
    op.drop_table('matchmaking_results')
    op.rename_table('matchmaking_results_new', 'matchmaking_results')


def downgrade() -> None:
    # Create old table structure
    op.create_table(
        'matchmaking_results_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bride_name', sa.String(length=100), nullable=False),
        sa.Column('bride_dob', sa.Date(), nullable=False),
        sa.Column('bride_tob', sa.Time(), nullable=False),
        sa.Column('bride_place_id', sa.Integer(), nullable=False),
        sa.Column('groom_name', sa.String(length=100), nullable=False),
        sa.Column('groom_dob', sa.Date(), nullable=False),
        sa.Column('groom_tob', sa.Time(), nullable=False),
        sa.Column('groom_place_id', sa.Integer(), nullable=False),
        sa.Column('compatibility_score', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('compatibility', sa.String(length=50), nullable=False),
        sa.Column('remarks', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['bride_place_id'], ['places.id'], ),
        sa.ForeignKeyConstraint(['groom_place_id'], ['places.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Copy data back
    op.execute('''
        INSERT INTO matchmaking_results_old (
            id, bride_name, bride_dob, bride_tob, bride_place_id,
            groom_name, groom_dob, groom_tob, groom_place_id,
            compatibility_score, compatibility, remarks, created_at
        )
        SELECT 
            id, bride_name, bride_dob, bride_tob, bride_place_id,
            groom_name, groom_dob, groom_tob, groom_place_id,
            compatibility_score, compatibility, remarks, created_at
        FROM matchmaking_results
    ''')

    # Drop new table and rename old table back
    op.drop_table('matchmaking_results')
    op.rename_table('matchmaking_results_old', 'matchmaking_results')
