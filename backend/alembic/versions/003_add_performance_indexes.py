"""Add performance indexes for faster queries

Revision ID: 003_add_performance_indexes
Revises: b04e4c16f1ae
Create Date: 2026-06-24 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '003_add_performance_indexes'
down_revision: Union[str, None] = 'b04e4c16f1ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create indexes for ThreadTaskPlan queries
    op.create_index('ix_thread_task_plan_status', 'thread_task_plans', ['thread_task_id', 'status'], unique=False)
    
    # Create index for ThreadTaskMemoryEntry queries
    op.create_index('ix_thread_task_memory_task', 'thread_task_memory_entries', ['thread_task_id'], unique=False)
    
    # Create index for ThreadMessage created_at (for sorting)
    op.create_index('ix_thread_messages_created_at', 'thread_messages', ['created_at'], unique=False)
    
    # Create index for PlanSubtask ordering
    op.create_index('ix_plan_subtask_ordering', 'plan_subtasks', ['thread_task_plan_id', 'ordering'], unique=False)


def downgrade() -> None:
    # Drop all created indexes
    op.drop_index('ix_plan_subtask_ordering', table_name='plan_subtasks')
    op.drop_index('ix_thread_messages_created_at', table_name='thread_messages')
    op.drop_index('ix_thread_task_memory_task', table_name='thread_task_memory_entries')
    op.drop_index('ix_thread_task_plan_status', table_name='thread_task_plans')
