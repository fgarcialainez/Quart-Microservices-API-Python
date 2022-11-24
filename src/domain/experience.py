import abc
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float, Boolean

from domain.base import AbstractTable


class ExperienceModel(BaseModel):
    """Experience Pydantic model"""
    id: str
    name: str
    stock: int
    price: float
    available: bool
    partner_id: str

    # Retrieved from partners service
    sold_tickets: Optional[int]


class Experience(AbstractTable):
    """Experience SQLAlchemy ORM table"""
    __tablename__ = "experience"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    # Mark if the experience is available for sale
    available = Column(Boolean, nullable=False)

    # Foreign key to the partners' table in the partners db
    partner_id = Column(String, nullable=False)


class ExperienceRepository(abc.ABC):
    @abc.abstractmethod
    async def get_customer_experiences(self) -> [ExperienceModel]:
        """Get all the experiences on sale with stock available"""
        pass

    @abc.abstractmethod
    async def get_partner_experiences(self, partner_id: str) -> [ExperienceModel]:
        """Get all the experiences for a given partner"""
        pass

    @abc.abstractmethod
    async def get_experience(self, experience_id: str) -> ExperienceModel:
        """Get an experience by identifier"""
        pass

    @abc.abstractmethod
    async def update_experience(self, experience_id: str, capacity: int | None, available: bool | None) -> str:
        """Update a experience data"""
        pass
