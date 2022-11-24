import abc


class PaymentsServiceInterface(abc.ABC):
    """Interface to abstract access to the payments external service"""

    @abc.abstractmethod
    def perform_payment(self, experience_id: str, price: float, quantity: int) -> None:
        """Performs a payment during the booking process"""
        pass
