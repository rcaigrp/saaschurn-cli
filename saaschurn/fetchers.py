import os
import requests
import time


class StripeFetcher:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://api.stripe.com/v1"

    def fetch_subscriptions(self):
        subscriptions = []
        url = f"{self.base_url}/subscriptions"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"status": "active"}

        while True:
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 429:
                    time.sleep(2)
                    continue
                if response.status_code != 200:
                    raise Exception(f"Stripe API error: {response.status_code}")
                data = response.json()
                subscriptions.extend(data.get("data", []))
                if not data.get("has_more"):
                    break
                url = data.get("next_page_url") or data.get("url")
            except Exception as e:
                raise e
        return subscriptions


class SlackFetcher:
    def __init__(self, token):
        self.token = token
        self.base_url = "https://slack.com/api"

    def fetch_channel_activity(self, channel_id):
        url = f"{self.base_url}/conversations.history"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"channel": channel_id, "limit": 100}

        messages = []
        while True:
            try:
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 429:
                    time.sleep(2)
                    continue
                if response.status_code != 200:
                    raise Exception(f"Slack API error: {response.status_code}")
                data = response.json()
                messages.extend(data.get("messages", []))
                if not data.get("response_metadata", {}).get("next_cursor"):
                    break
                params["cursor"] = data.get("response_metadata", {}).get("next_cursor")
            except Exception as e:
                raise e
        return messages
