import injector

from application.services.partners_service import PartnersServiceInterface
from application.services.payments_service import PaymentsServiceInterface
from domain.experience import ExperienceRepository
from infrastructure.partners_adapter import PartnersServiceAdapter
from infrastructure.payments_adapter import PaymentsServiceAdapter
from infrastructure.postgres_adapter import ExperiencePostgresAdapter
from infrastructure.redis_adapter import RedisAdapter
from infrastructure.cache import CacheInterface


def configure(binder: injector.Binder) -> None:
    """Configure dependencies injection"""
    binder.bind(PartnersServiceInterface, to=PartnersServiceAdapter)
    binder.bind(PaymentsServiceInterface, to=PaymentsServiceAdapter)
    binder.bind(ExperienceRepository, to=ExperiencePostgresAdapter)
    binder.bind(CacheInterface, to=RedisAdapter)
