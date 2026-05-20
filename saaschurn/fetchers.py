import requests
import time

class StripeFetcher:
    def __init__(self, token, base_url="https://api.stripe.com/v1"):
        self.token = token
        self.base_url = base_url

    def fetch_active_subscriptions(self):
        url = f"{self.base_url}/subscriptions"
        params = {"status": "active", "limit": 100}
        subscriptions = []
        while True:
            response = requests.get(url, headers={"Authorization": f"Bearer {self.token}"}, params=params)
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                time.sleep(retry_after)
                continue
            if response.status_code != 200:
                raise Exception(f"Stripe API error: {response.status_code}")
            data = response.json()
            subscriptions.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            params["starting_after"] = data.get("data")[-1]["id"]
        return subscriptions

class SlackFetcher:
    def __init__(self, token, base_url="https://slack.com/api"):
        self.token = token
        self.base_url = base_url

    def fetch_channel_activity(self, channel_id):
        url = f"{self.base_url}/conversations.history"
        params = {"channel": channel_id, "limit": 1000}
        response = requests.get(url, headers={"Authorization": f"Bearer {self.token}"}, params=params)
        if response.status_code == 429:
            time.sleep(int(response.headers.get('Retry-After', 1)))
            return 0
        if response.status_code != 200:
            return 0
        data = response.json()
        messages = data.get("messages", [])
        return len(messages)
