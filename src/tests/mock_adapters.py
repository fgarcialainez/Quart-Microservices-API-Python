from application.services.partners_service import PartnersServiceInterface
from application.services.payments_service import PaymentsServiceInterface
from infrastructure.cache import CacheInterface


class MockPartnersServiceAdapter(PartnersServiceInterface):
    """Mock implementation of the PartnersServiceInterface"""
    def send_booking_to_partner(self, experience_id: str, quantity: int) -> None:
        """Send a booking to a partner"""
        pass

    def get_experience_sold_tickets(self, experience_id: str) -> int | None:
        """Get the number of sold tickets for a given experience calling the partners service API"""
        return 10


class MockPaymentsServiceAdapter(PaymentsServiceInterface):
    """Mock implementation of the PaymentsServiceInterface"""
    def perform_payment(self, experience_id: str, price: float, quantity: int) -> None:
        """Performs a payment during the experience booking process"""
        pass


class MockCacheAdapter(CacheInterface):
    """Mock implementation of the CacheInterface"""
    def get(self, key: str):
        """Get data for a given key"""
        pass

    def set(self, key: str, data: str):
        """Set data for a given key"""
        pass

    def invalidate(self, key: str) -> None:
        """Invalidate the entry for a given key"""
        pass

    def invalidate_key_pattern(self, pattern: str):
        """Invalidate all the keys that match the pattern param"""
        pass
