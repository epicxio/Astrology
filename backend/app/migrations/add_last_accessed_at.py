"""Add last_accessed_at column to matchmaking_results table"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic
revision = 'add_last_accessed_at'
down_revision = None  # Update this to your last migration
branch_labels = None
depends_on = None

def upgrade():
    # Add last_accessed_at column with default value
    op.add_column('matchmaking_results',
        sa.Column('last_accessed_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'))
    )

def downgrade():
    # Remove last_accessed_at column
    op.drop_column('matchmaking_results', 'last_accessed_at') 