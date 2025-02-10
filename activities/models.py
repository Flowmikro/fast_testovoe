from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, Integer

from typing import List, Optional

import conf

organization_activity_association = Table(
    'organization_activity',
    conf.Base.metadata,
    Column('organization_id',
           Integer,
           ForeignKey('organization.id'),
           primary_key=True
           ),
    Column('activity_id',
           Integer,
           ForeignKey('activity.id'),
           primary_key=True
           ),
    extend_existing=True
)


class ActivityModel(conf.Base):
    __tablename__ = "activity"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("activity.id"), nullable=True)

    parent: Mapped[Optional["ActivityModel"]] = relationship(
        "ActivityModel", remote_side=[id], back_populates="children"
    )
    children: Mapped[List["ActivityModel"]] = relationship(
        "ActivityModel", back_populates="parent", cascade="all, delete-orphan"
    )
    organizations: Mapped[list["OrganizationModel"]] = relationship(
        "OrganizationModel",
        secondary=organization_activity_association,
        back_populates="activities"
    )

    def level(self) -> int:
        level = 0
        parent = self.parent
        while parent:
            level += 1
            if level >= 3:
                raise ValueError("Максимальный уровень вложенности — 3")
            parent = parent.parent
        return level
