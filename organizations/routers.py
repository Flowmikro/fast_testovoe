import conf

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends

from .services import Service

router = APIRouter()


@router.get("/organizations")
async def get_all_organizations(
        session: AsyncSession = Depends(conf.get_session)
):
    """
    Список всех организаций
    """
    return await Service.get_all_organizations_query(session)


