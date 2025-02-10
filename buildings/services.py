from math import cos

from geopy.units import radians
from starlette import status
from starlette.responses import JSONResponse

import conf

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends

from buildings.models import BuildingModel
from organizations.models import OrganizationModel


class Service:
    @classmethod
    async def get_organizations_address(
            cls,
            address: str,
            session: AsyncSession = Depends(conf.get_session),
    ) -> JSONResponse:
        stmt = (
            select(OrganizationModel.name)
            .join(BuildingModel, OrganizationModel.building_id == BuildingModel.id)
            .where(BuildingModel.address == address)
        )
        result = await session.execute(stmt)
        return JSONResponse(content={"data": result.scalars().all()}, status_code=status.HTTP_200_OK)

    @classmethod
    async def get_organization_by_name(
            cls,
            organization_name: str,
            session: AsyncSession = Depends(conf.get_session),
    ) -> JSONResponse:
        stmt = await session.execute(
            select(OrganizationModel.name).filter(OrganizationModel.name == organization_name)
        )
        result = stmt.scalars().all()
        return JSONResponse(content={"data": result}, status_code=status.HTTP_200_OK)

    @classmethod
    async def get_organization_by_id(
            cls,
            organization_id: int,
            session: AsyncSession = Depends(conf.get_session)
    ) -> JSONResponse:
        stmt = await session.execute(
            select(OrganizationModel.name).filter(OrganizationModel.id == organization_id)
        )
        result = stmt.scalars().all()
        return JSONResponse(content={"data": result}, status_code=status.HTTP_200_OK)

    @classmethod
    async def get_organizations_within_radius(
            cls,
            latitude: float,
            longitude: float,
            radius_km: float,
            session: AsyncSession = Depends(conf.get_session),
    ):
        radius_deg = radius_km / 111.32

        lat_min = latitude - radius_deg
        lat_max = latitude + radius_deg
        lon_min = longitude - radius_deg / abs(cos(radians(latitude)))
        lon_max = longitude + radius_deg / abs(cos(radians(latitude)))

        stmt = (
            select(OrganizationModel)
            .join(BuildingModel)
            .filter(
                BuildingModel.latitude.between(lat_min, lat_max),
                BuildingModel.longitude.between(lon_min, lon_max),
            )
        )

        result = await session.execute(stmt)
        return result.scalars().all()
