from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.helpers import row_to_model_list
from infrastructure.database import session_factory
from domain.experience import Experience, ExperienceModel, ExperienceRepository


class ExperiencePostgresAdapter(ExperienceRepository):
    """PostgreSQL implementation of the ExperienceRepository"""
    def __init__(self):
        self.session_factory = session_factory()

    async def _get_experience(self, session: AsyncSession, experience_id: str, for_update: bool) -> Experience:
        """Get an experience by identifier"""
        if for_update:
            statement = select(Experience).where(Experience.id == experience_id).with_for_update()
        else:
            statement = select(Experience).where(Experience.id == experience_id)

        results = await session.execute(statement)
        return next(results)[0]

    async def get_customer_experiences(self) -> [ExperienceModel]:
        """Get all the experiences on sale with stock available"""
        async with session_factory() as session:
            statement = select(Experience).where(Experience.stock > 0).where(Experience.available.is_(True))
            results = await session.execute(statement)
            return row_to_model_list(results.scalars(), ExperienceModel)

    async def get_partner_experiences(self, partner_id: str) -> [ExperienceModel]:
        """Get all the experiences for a given partner"""
        async with session_factory() as session:
            statement = select(Experience).where(Experience.partner_id == partner_id)
            results = await session.execute(statement)
            return row_to_model_list(results.scalars(), ExperienceModel)

    async def get_experience(self, experience_id: str) -> ExperienceModel:
        """Get an experience by identifier"""
        async with session_factory() as session:
            experience = await self._get_experience(session, experience_id, False)
            return ExperienceModel.parse_obj(experience.as_dict())

    async def update_experience(self, experience_id: str, capacity: int | None, available: bool | None) -> str:
        """Update a experience data"""
        async with session_factory() as session:
            # Begin the transaction
            session.begin()

            # Get the experience to update
            experience = await self._get_experience(session, experience_id, True)

            # Update experience data
            if capacity is not None:
                if capacity >= 0:
                    experience.stock = capacity
                else:
                    return "Capacity value can't be negative."

            if available is not None:
                experience.available = available

            session.add(experience)

            # Commit the transaction
            await session.commit()
