from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

import conf
from .services import Service

router = APIRouter()


@router.get('/search/organization/{activity_name}')
async def search_organization(
        activity_name: Optional[str] = None,
        session: AsyncSession = Depends(conf.get_session)
):
    """
    Поиск организаций по деятельности
    """
    return await Service.search_organization(activity_name, session)
