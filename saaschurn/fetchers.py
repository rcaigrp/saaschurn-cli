import requests
import time

class StripeFetcher:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.stripe.com/v1/subscriptions"

    def fetch_subscriptions(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        subscriptions = []
        cursor = None
        while True:
            params = {"limit": 100}
            if cursor:
                params["starting_after"] = cursor
            try:
                response = requests.get(self.base_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.HTTPError as e:
                if e.response and e.response.status_code == 429:
                    time.sleep(2 ** e.response.json().get('error', {}).get('retry_after', 5))
                    continue
                raise
            except Exception:
                raise
            subscriptions.extend(data.get('data', []))
            if not data.get('has_more'):
                break
            cursor = data.get('next_starting_after')
        return subscriptions

class SlackFetcher:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.slack.com/methods/conversations.list"
        self.history_url = "https://api.slack.com/methods/conversations.history"

    def get_channels(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        channels = []
        cursor = None
        while True:
            params = {"limit": 100}
            if cursor:
                params["cursor"] = cursor
            try:
                response = requests.get(self.base_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
            except Exception:
                return []
            channels.extend([c["id"] for c in data.get("conversations", [])])
            if not data.get("response_metadata", {}).get("next_cursor"):
                break
            cursor = data.get("response_metadata", {}).get("next_cursor")
        return channels

    def get_channel_activity(self, channels):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        activity = {}
        for channel_id in channels:
            params = {"channel": channel_id, "limit": 1000}
            try:
                response = requests.get(self.history_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                messages = data.get("messages", [])
                activity[channel_id] = len(messages)
            except Exception:
                activity[channel_id] = 0
        return activity
