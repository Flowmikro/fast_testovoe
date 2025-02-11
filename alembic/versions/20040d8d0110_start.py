"""Start

Revision ID: 20040d8d0110
Revises: 
Create Date: 2025-02-11 00:59:13.363326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '20040d8d0110'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('parent_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['parent_id'], ['activity.id'],
                                            name=op.f('fk__activity__parent_id__activity')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__activity')),
                    sa.UniqueConstraint('id', name=op.f('uq__activity__id')),
                    sa.UniqueConstraint('name', name=op.f('uq__activity__name'))
                    )
    op.create_table('building',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('latitude', sa.Float(), nullable=False),
                    sa.Column('longitude', sa.Float(), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__building')),
                    sa.UniqueConstraint('id', name=op.f('uq__building__id'))
                    )
    op.create_table('organization',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('phone_numbers', sa.JSON(), nullable=False),
                    sa.Column('building_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['building_id'], ['building.id'],
                                            name=op.f('fk__organization__building_id__building')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk__organization')),
                    sa.UniqueConstraint('id', name=op.f('uq__organization__id'))
                    )
    op.create_table('organization_activity',
                    sa.Column('organization_id', sa.Integer(), nullable=False),
                    sa.Column('activity_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['activity_id'], ['activity.id'],
                                            name=op.f('fk__organization_activity__activity_id__activity')),
                    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'],
                                            name=op.f('fk__organization_activity__organization_id__organization')),
                    sa.PrimaryKeyConstraint('organization_id', 'activity_id', name=op.f('pk__organization_activity'))
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organization_activity')
    op.drop_table('organization')
    op.drop_table('building')
    op.drop_table('activity')
    # ### end Alembic commands ###
