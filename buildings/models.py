from sqlalchemy.orm import Mapped, mapped_column, relationship

import conf


class BuildingModel(conf.Base):
    __tablename__ = 'building'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    address: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]

    organization: Mapped[list["OrganizationModel"]] = relationship(
        back_populates='building',
    )
