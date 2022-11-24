from enum import Enum
from typing import List

from quart import json

from application.services.partners_service import PartnersServiceInterface
from application.services.payments_service import PaymentsServiceInterface
from domain.experience import ExperienceModel, ExperienceRepository
from domain.helpers import dict_to_model_list, model_to_dict_list
from infrastructure.cache import CacheInterface


class CacheKeys(str, Enum):
    EXPERIENCES_LIST = "EXPERIENCES_LIST"

    @staticmethod
    def get_experiences_list_cache_key(partner_id: str):
        if not partner_id:
            return f"{CacheKeys.EXPERIENCES_LIST}"
        return f"{CacheKeys.EXPERIENCES_LIST}:{partner_id}"


class ExperienceService:
    def __init__(self,
                 partners: PartnersServiceInterface,
                 payments: PaymentsServiceInterface,
                 repository: ExperienceRepository,
                 cache: CacheInterface):
        """Initialize the service passing the dependencies"""
        self.partners_service = partners
        self.payments_service = payments
        self.repository = repository
        self.cache = cache

    async def get_experiences_list(self, partner_id: str = None) -> List[ExperienceModel]:
        # Get the cache key
        cache_key = CacheKeys.get_experiences_list_cache_key(partner_id)

        # Check if data exists in cache
        json_data = self.cache.get(cache_key)

        if not json_data:
            # Fetch data from db
            if partner_id:
                experiences = await self.repository.get_partner_experiences(partner_id)
            else:
                experiences = await self.repository.get_customer_experiences()

            # Call the partners service to get the number of sold tickets for all the experiences.
            # Note that this approach won't perform well, so it should be improved aggregating
            # partners service data with experiences data using patterns as for example CQRS. Other
            # (better) option could be to send a list of experience ids and get an object with keys
            # equal to the experience id and values the number of sold tickets for each experience.
            if partner_id:
                for experience in experiences:
                    sold_tickets = self.partners_service.get_experience_sold_tickets(experience.id)
                    experience.sold_tickets = sold_tickets if sold_tickets else 0

            # Convert model list to dict list. Note that could be returned the dict list
            # directly from the repository and save an additional conversion, but the
            # repository interface wouldn't be as clear as with returning the model list.
            dict_list = model_to_dict_list(experiences)

            # Stora data in cache
            self.cache.set(cache_key, json.dumps(dict_list))
        else:
            # Create the dict list from the JSON data
            dict_list = json.loads(json_data)
            experiences = dict_to_model_list(dict_list, ExperienceModel)

        # Return the list of experiences
        return experiences

    async def get_experience(self, experience_id: str) -> ExperienceModel:
        # Check if data exists in cache
        json_data = self.cache.get(experience_id)

        if not json_data:
            # Fetch data from db
            experience = await self.repository.get_experience(experience_id)

            # Call the partners service to get the number of sold tickets for the experience.
            # Note that this approach is not the best, so it should be improved aggregating
            # partners service data with experiences data using patterns as for example CQRS.
            sold_tickets = self.partners_service.get_experience_sold_tickets(experience_id)
            experience.sold_tickets = sold_tickets if sold_tickets else 0

            # Save the experience in cache
            self.cache.set(experience_id, json.dumps(experience.dict()))
        else:
            # Create the experience model from the JSON data
            dict_obj = json.loads(json_data)
            experience = ExperienceModel.parse_obj(dict_obj)

        # Return the experience
        return experience

    async def update_experience(self, experience_id: str, capacity: int | None, available: bool | None) -> str:
        """Update an experience"""

        # Update the experience
        error_msg = await self.repository.update_experience(experience_id, capacity, available)

        if not error_msg:
            # Invalidate the cache
            self._invalidate_cache(experience_id)

        # Return the error msg (None = success)
        return error_msg

    async def book_experience(self, experience_id: str, quantity: int):
        """Book and experience"""

        # Get the experience to book
        experience = await self.repository.get_experience(experience_id)

        # Check there is enough stock
        if not self._has_enough_experience_stock(experience, quantity):
            return "Not enough experience stock"

        # Call the external service to perform the payment
        self.payments_service.perform_payment(experience_id, experience.price, quantity)

        # Descrease experience stock
        await self._decrease_experience_stock(experience, quantity)

        # Call the external service to send the booking to the partner
        self.partners_service.send_booking_to_partner(experience_id, quantity)

        # Invalidate the cache
        self._invalidate_cache(experience_id)

    def _has_enough_experience_stock(self, experience: ExperienceModel, requested_quantity: int) -> bool:
        return experience.stock >= requested_quantity

    async def _decrease_experience_stock(self, experience: ExperienceModel, quantity: int) -> None:
        # Calculate the new stock
        stock = experience.stock - quantity

        # UPdate the stock in db
        await self.repository.update_experience(experience.id, stock, None)

    def _invalidate_cache(self, experience_id: str):
        self.cache.invalidate_key_pattern(CacheKeys.EXPERIENCES_LIST)
        self.cache.invalidate(experience_id)
