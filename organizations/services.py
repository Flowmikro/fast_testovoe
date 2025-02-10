import conf

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .models import OrganizationModel


class Service:
    @classmethod
    async def get_all_organizations_query(
            cls,
            session: AsyncSession = Depends(conf.get_session)
    ):
        stmt = await session.execute(
            select(OrganizationModel)
        )
        result = stmt.scalars().all()
        return JSONResponse(content={"data": jsonable_encoder(result)},
                            status_code=status.HTTP_200_OK)
