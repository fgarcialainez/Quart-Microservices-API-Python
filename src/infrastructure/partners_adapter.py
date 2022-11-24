import requests


class PartnersServiceAdapter:
    def send_booking_to_partner(self, experience_id: str, quantity: int) -> None:
        """Send a booking to a partner"""
        response = requests.post("https://partner-service.free.beeceptor.com/purchase")
        if response.status_code != 200:
            raise Exception("Problem sending the purchase to the partner")

    def get_experience_sold_tickets(self, experience_id: str) -> int | None:
        """Get the number of sold tickets for a given experience calling the partners service API"""
        response = requests.get("https://partner-service.free.beeceptor.com/soldtickets")
        if response.status_code != 200:
            raise Exception("Problem retrieving the number of sold tickets from the partner")
        return None
