import abc


class PartnersServiceInterface(abc.ABC):
    """Interface to abstract access to the partners external service"""

    @abc.abstractmethod
    def send_booking_to_partner(self, experience_id: str, quantity: int) -> None:
        """Send a booking to a partner"""
        pass

    @abc.abstractmethod
    def get_experience_sold_tickets(self, experience_id: str) -> int | None:
        """Get the number of sold tickets for a given experience calling the partners service API"""
        pass
