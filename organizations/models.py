import conf
from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from activities.models import organization_activity_association


class OrganizationModel(conf.Base):
    __tablename__ = "organization"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]
    phone_numbers: Mapped[dict] = mapped_column(JSON, nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"))

    building: Mapped["BuildingModel"] = relationship(
        back_populates='organization'
    )

    activities: Mapped[list["ActivityModel"]] = relationship(
        "ActivityModel",
        secondary=organization_activity_association,
        back_populates="organizations"
    )
