import os
import time
import requests


class StripeFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stripe.com/v1/subscriptions"
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def fetch_subscriptions(self):
        subscriptions = []
        params = {"status": "active"}
        while True:
            res = requests.get(self.base_url, headers=self.headers, params=params)
            res.raise_for_status()
            data = res.json()
            subscriptions.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            params["starting_after"] = data.get("latest_cursor")
            time.sleep(0.5)
        return subscriptions


class SlackFetcher:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://slack.com/api/conversations.history"
        self.headers = {"Authorization": f"Bearer {token}"}

    def fetch_channel_activity(self, channel_id, days=30):
        params = {"channel": channel_id, "count": 1000}
        res = requests.get(self.base_url, headers=self.headers, params=params)
        res.raise_for_status()
        data = res.json()
        messages = data.get("messages", [])
        total_msgs = sum(m.get("num_messages", 0) for m in messages)
        return total_msgs