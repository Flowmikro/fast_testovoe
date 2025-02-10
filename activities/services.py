from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, status
from fastapi.responses import JSONResponse

import conf
from activities.models import ActivityModel, organization_activity_association
from organizations.models import OrganizationModel


class Service:
    @classmethod
    async def search_organization(
            cls,
            activity_name: str,
            session: AsyncSession = Depends(conf.get_session)
    ) -> JSONResponse:
        async def fetch_ids(query):
            result = await session.execute(query)
            return [row[0] for row in result.all()]

        parent_ids = await fetch_ids(select(ActivityModel.id).filter(ActivityModel.name == activity_name))
        if not parent_ids:
            return JSONResponse(content={"msg": "Не найдено"}, status_code=status.HTTP_404_NOT_FOUND)

        child_ids = await fetch_ids(select(ActivityModel.id).filter(ActivityModel.parent_id.in_(parent_ids)))
        target_ids = child_ids if child_ids else parent_ids

        organization_ids = await fetch_ids(select(organization_activity_association.c.organization_id).filter(
            organization_activity_association.c.activity_id.in_(target_ids)
        ))
        if not organization_ids:
            return JSONResponse(content={"msg": "Не найдено"}, status_code=status.HTTP_200_OK)

        organizations = await fetch_ids(
            select(OrganizationModel.name).filter(OrganizationModel.id.in_(organization_ids)))
        return JSONResponse(content={"data": organizations}, status_code=status.HTTP_200_OK)
