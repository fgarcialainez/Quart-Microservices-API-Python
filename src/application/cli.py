from asyncio import get_event_loop
from random import randint, random
from uuid import uuid4

from click import command

from infrastructure.database import engine, Base, session_factory
from domain.experience import Experience

# Fixed set of experiences and partners for tests
TEST_EXPERIENCE_ID_1 = "d9b0088a-4e5f-4bd3-8583-4bd3954588e6"
TEST_EXPERIENCE_ID_2 = "5c357098-3b78-491f-a1c4-bc76fbbc182e"
TEST_PARTNER_ID_WITH_EXPERIENCES = "32a58593-b6e6-40d2-8d05-7bf6a1068a7f"
TEST_PARTNER_ID_WITHOUT_EXPERIENCES = "3da4b51c-4312-490f-8116-e364352f738f"


@command()
def populate_db() -> None:
    get_event_loop().run_until_complete(__populate_db())


async def __populate_db() -> None:
    connexion = await engine.connect()
    connexion.begin()
    await connexion.run_sync(Base.metadata.create_all)
    await connexion.commit()
    await connexion.close()
    session = session_factory()
    session.begin()
    session.add_all(
        [
            Experience(
                id=str(uuid4()),
                name="Test experience 1",
                stock=randint(0, 10),
                price=random(),
                available=True,
                partner_id=str(uuid4())
            ),
            Experience(
                id=str(uuid4()),
                name="Test experience 2",
                stock=randint(0, 10),
                price=random(),
                available=True,
                partner_id=str(uuid4())
            ),
            Experience(
                id=str(uuid4()),
                name="Test experience 3",
                stock=randint(0, 10),
                price=random(),
                available=False,
                partner_id=str(uuid4())
            ),
            Experience(
                id=TEST_EXPERIENCE_ID_1,
                name="Test experience 4",
                stock=randint(0, 10),
                price=random(),
                available=True,
                partner_id=TEST_PARTNER_ID_WITH_EXPERIENCES
            ),
            Experience(
                id=TEST_EXPERIENCE_ID_2,
                name="Test experience 5",
                stock=randint(0, 10),
                price=random(),
                available=True,
                partner_id=TEST_PARTNER_ID_WITH_EXPERIENCES
            ),
        ]
    )
    await session.commit()
    await session.close()


@command()
def drop_db() -> None:
    get_event_loop().run_until_complete(__drop_db())


async def __drop_db() -> None:
    connexion = await engine.connect()
    connexion.begin()
    await connexion.run_sync(Base.metadata.drop_all)
    await connexion.commit()
    await connexion.close()
