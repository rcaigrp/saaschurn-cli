import requests

class StripeClient:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://api.stripe.com/v1/subscriptions'

    def get_active_subscriptions(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'status': 'active'}
        resp = requests.get(self.api_url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()['data']
