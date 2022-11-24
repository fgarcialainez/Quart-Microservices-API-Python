import requests


class PaymentsServiceAdapter:
    def perform_payment(self, experience_id: str, price: float, quantity: int) -> None:
        """Performs a payment during the experience booking process"""
        response = requests.post("https://payment-provider.free.beeceptor.com/pay")
        if response.status_code != 200:
            raise Exception("Problem with the payment")
