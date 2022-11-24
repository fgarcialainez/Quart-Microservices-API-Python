import injector
import pytest
import quart_injector

from ..app import app
from application.services.payments_service import PaymentsServiceInterface
from .mock_adapters import MockPartnersServiceAdapter, MockCacheAdapter, MockPaymentsServiceAdapter
from application.services.partners_service import PartnersServiceInterface
from domain.experience import ExperienceRepository
from infrastructure.postgres_adapter import ExperiencePostgresAdapter
from infrastructure.cache import CacheInterface


def configure(binder: injector.Binder) -> None:
    """Configure dependencies injection for testing"""
    binder.bind(PartnersServiceInterface, to=MockPartnersServiceAdapter)
    binder.bind(PaymentsServiceInterface, to=MockPaymentsServiceAdapter)
    binder.bind(ExperienceRepository, to=ExperiencePostgresAdapter)
    binder.bind(CacheInterface, to=MockCacheAdapter)


@pytest.fixture(name='test_client', scope="module")
def _test_client():
    # Wire the app to the injector configuration for testing
    quart_injector.wire(app, configure)

    # Return the test client
    return app.test_client()
