from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from conf import get_session
from .services import Service

router = APIRouter()


@router.get('/get/address')
async def get_organizations_address(
        address: str,
        session: AsyncSession = Depends(get_session),
):
    """
    Поиск организации по адресу
    """
    return await Service.get_organizations_address(
        address, session
    )

@router.get('/get/within-radius')
async def get_organizations_within_radius(
        latitude: float,
        longitude: float,
        radius_km: float,
        session: AsyncSession = Depends(get_session),
):
    """
    Поиск организации по заданным координатам
    """
    return await Service.get_organizations_within_radius(
        latitude, longitude, radius_km, session
    )


@router.get('/get/id/{organization_id}')
async def get_organizations(
        organization_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Получить организацию по ее id
    """
    return await Service.get_organization_by_id(organization_id, session)


@router.get('/get/name/{organization_name}')
async def get_organization(
        organization_name: str,
        session: AsyncSession = Depends(get_session),
):
    """
    Поиск организации по ее названию
    """
    return await Service.get_organization_by_name(organization_name, session)
