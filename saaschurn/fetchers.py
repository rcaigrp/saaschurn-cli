import requests
import os
import time

class StripeFetcher:
    def __init__(self):
        self.api_key = os.getenv("STRIPE_API_KEY")
        self.url = "https://api.stripe.com/v1/subscriptions"
    
    def fetch_subscriptions(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"limit": 100}
        subscriptions = []
        while True:
            try:
                resp = requests.get(self.url, headers=headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                subscriptions.extend(data.get("data", []))
                if not data.get("has_more"):
                    break
                params["starting_after"] = data.get("data")[-1]["id"]
                time.sleep(0.1) # Rate limit handling
            except requests.exceptions.HTTPError as e:
                print(f"Stripe API Error: {e}")
                break
        return subscriptions

class SlackFetcher:
    def __init__(self):
        self.api_key = os.getenv("SLACK_API_KEY")
        self.url = "https://slack.com/api/conversations.history"
    
    def fetch_activity(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        channels = self._get_channels()
        activity = {}
        for channel in channels:
            try:
                params = {"channel": channel["id"], "limit": 100}
                resp = requests.get(self.url, headers=headers, params=params)
                resp.raise_for_status()
                data = resp.json()
                msgs = len(data.get("messages", []))
                activity[channel["name"]] = msgs
            except requests.exceptions.HTTPError as e:
                print(f"Slack API Error for {channel['name']}: {e}")
        return activity
    
    def _get_channels(self):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"limit": 100}
        channels = []
        while True:
            resp = requests.get("https://slack.com/api/conversations.list", headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            channels.extend(data.get("channels", []))
            if not data.get("is_truncated"):
                break
            params["cursor"] = data.get("response_metadata")["next_cursor"]
        return channels
