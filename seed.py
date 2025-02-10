from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

import asyncio
from conf import OrganizationModel, BuildingModel, ActivityModel, organization_activity_association
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from conf import settings

DATABASE_URL_TEST = settings.database_url

engine = create_async_engine(DATABASE_URL_TEST)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


async def main():
    async with async_session_maker() as session:
        try:
            session.add(BuildingModel(address="Moscow, Tverskaya St., 1", latitude=55.7558, longitude=37.6173))
            session.add(BuildingModel(address="Saint Petersburg, Nevsky Ave., 2", latitude=59.9343, longitude=30.3351))
            session.add(BuildingModel(address="Moscow, Tverskaya St., 1", latitude=55.7558, longitude=37.6173))
            session.add(BuildingModel(address="Saint Petersburg, Nevsky Ave., 2", latitude=59.9343, longitude=30.3351))
            session.add(BuildingModel(address="Yekaterinburg, Lenin St., 3", latitude=56.8389, longitude=60.6056))
            session.add(BuildingModel(address="Kazan, Bauman St., 4", latitude=55.8304, longitude=49.0661))
            session.add(BuildingModel(address="Novosibirsk, Krasny Prospekt, 5", latitude=55.0084, longitude=82.9357))
            await session.commit()

            activities = [
                ActivityModel(name="Sports"),
                ActivityModel(name="IT"),
                ActivityModel(name="Frontend", parent_id=2),
                ActivityModel(name="Backend", parent_id=2),
                ActivityModel(name="Art"),
                ActivityModel(name="Education")
            ]

            session.add_all(activities)
            await session.commit()

            organizations = [
                OrganizationModel(name="Organization 1", phone_numbers={"office": "+7 123 456-78-90"}, building_id=1),
                OrganizationModel(name="Organization 2", phone_numbers={"office": "+7 123 456-78-91"}, building_id=2),
                OrganizationModel(name="Organization 3", phone_numbers={"office": "+7 123 456-78-92"}, building_id=3),
                OrganizationModel(name="Organization 4", phone_numbers={"office": "+7 123 456-78-93"}, building_id=4),
                OrganizationModel(name="Organization 5", phone_numbers={"office": "+7 123 456-78-94"}, building_id=5)
            ]

            session.add_all(organizations)
            await session.commit()

            org_activity_association_data = [
                {"organization_id": 1, "activity_id": 1},
                {"organization_id": 2, "activity_id": 2},
                {"organization_id": 3, "activity_id": 3},
                {"organization_id": 4, "activity_id": 4},
                {"organization_id": 5, "activity_id": 3},
            ]

            stmt = insert(organization_activity_association).values(org_activity_association_data).returning(
                organization_activity_association.c.organization_id, organization_activity_association.c.activity_id
            )
            result = await session.execute(stmt)
            print("---###########END##########################")
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            print(f"Error occurred")

if __name__ == "__main__":
    asyncio.run(main())
