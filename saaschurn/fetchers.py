import requests
import time

class StripeFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stripe.com/v1/subscriptions"

    def fetch_active_subscriptions(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"limit": 100}
        all_subs = []
        while True:
            try:
                response = requests.get(self.base_url, headers=headers, params=params)
                if response.status_code == 429:
                    time.sleep(2 ** (response.status_code // 100))
                    continue
                response.raise_for_status()
                data = response.json()
                all_subs.extend(data.get("data", []))
                if not data.get("has_more"):
                    break
                params["starting_after"] = data.get("last_response", {}).get("data", [{}])[-1].get("id")
            except requests.exceptions.RequestException:
                break
        return all_subs

class SlackFetcher:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://slack.com/api/conversations.history"

    def fetch_channel_activity(self, channel_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"channel": channel_id, "limit": 100}
        try:
            response = requests.get(self.base_url, headers=headers, params=params)
            if response.status_code == 429:
                time.sleep(2)
                return self.fetch_channel_activity(channel_id)
            response.raise_for_status()
            return response.json().get("messages", [])
        except requests.exceptions.RequestException:
            return []
