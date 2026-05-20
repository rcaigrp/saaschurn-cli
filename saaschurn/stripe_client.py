import requests

class StripeClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.stripe.com/v1"

    def get_subscriptions(self):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        try:
            resp = requests.get(f"{self.base_url}/subscriptions", headers=headers)
            resp.raise_for_status()
            return resp.json().get("data", [])
        except Exception:
            return []
