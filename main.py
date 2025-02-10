import contextlib
from typing import AsyncIterator
from fastapi import FastAPI

import conf
from buildings.routers import router as building_router
from activities.routers import router as activities_router
from organizations.routers import router as organizations_router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    conf.db_manager.init(conf.settings.database_url)
    yield
    await conf.db_manager.close()


app = FastAPI(title="FastAPI", lifespan=lifespan)

app.include_router(building_router, prefix='/organizations')
app.include_router(activities_router, prefix='/organizations')
app.include_router(organizations_router, prefix='/organizations')
