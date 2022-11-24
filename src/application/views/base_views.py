import abc
from typing import List

from injector import Inject
from pydantic import BaseModel
from quart.views import MethodView

from application.services.experience_service import ExperienceModel, ExperienceService
from application.services.partners_service import PartnersServiceInterface
from application.services.payments_service import PaymentsServiceInterface
from domain.experience import ExperienceRepository
from infrastructure.cache import CacheInterface


class ExperienceListResponse(BaseModel):
    experiences: List[ExperienceModel]


class BaseExperienceMethodView(MethodView, abc.ABC):
    def __init__(self,
                 partners: Inject[PartnersServiceInterface],
                 payments: Inject[PaymentsServiceInterface],
                 repository: Inject[ExperienceRepository],
                 cache: Inject[CacheInterface]):
        """Initialize the service passing the injected adapters"""
        self.service = ExperienceService(partners, payments, repository, cache)
