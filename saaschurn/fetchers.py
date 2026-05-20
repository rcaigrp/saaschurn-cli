import requests
import time
import json
import os


class StripeFetcher:
    def __init__(self, stripe_api_key=None, mock=False):
        self.stripe_api_key = stripe_api_key
        self.mock = mock
        self.base_url = "https://api.stripe.com/v1/subscriptions"
        self.headers = {"Authorization": f"Bearer {stripe_api_key}"}

    def fetch_active_subscriptions(self):
        if self.mock:
            return self._get_mock_data()
        return self._fetch_subscriptions()

    def _fetch_subscriptions(self):
        params = {"status": "active"}
        subscriptions = []
        url = self.base_url

        while True:
            try:
                resp = requests.get(url, headers=self.headers, params=params)
                if resp.status_code == 429:
                    wait = 2 ** 1
                    time.sleep(wait)
                    continue

                if resp.status_code != 200:
                    raise Exception(f"Stripe API error: {resp.status_code}")

                data = resp.json()
                subscriptions.extend(data.get("data", []))

                if "next_page" in data:
                    url = data["next_page"]
                else:
                    break
            except Exception as e:
                raise e

        return subscriptions

    def _get_mock_data(self):
        return [
            {"id": "sub_1", "customer_id": "cus_1", "plan": {"id": "plan_1"}, "current_period_end": 1700000000, "amount": 1000},
            {"id": "sub_2", "customer_id": "cus_2", "plan": {"id": "plan_2"}, "current_period_end": 1700000000, "amount": 500},
        ]


class SlackFetcher:
    def __init__(self, slack_api_token=None, mock=False):
        self.slack_api_token = slack_api_token
        self.mock = mock
        self.base_url = "https://slack.com/api/conversations.history"
        self.headers = {"Authorization": f"Bearer {slack_api_token}"}
        self.channel_mapping = json.loads(os.getenv("SLACK_CHANNELS", "{}"))

    def fetch_channel_activity(self):
        if self.mock:
            return self._get_mock_data()
        return self._fetch_activity()

    def _fetch_activity(self):
        activity = []
        for customer_id, channel_id in self.channel_mapping.items():
            params = {"channel": channel_id}
            try:
                resp = requests.get(self.base_url, headers=self.headers, params=params)
                if resp.status_code == 429:
                    time.sleep(2)
                    continue

                if resp.status_code != 200:
                    continue

                data = resp.json()
                messages = data.get("messages", [])
                activity.append({"customer_id": customer_id, "channel_id": channel_id, "message_count": len(messages)})
            except Exception:
                continue
        return activity

    def _get_mock_data(self):
        return [
            {"customer_id": "cus_1", "channel_id": "C1", "message_count": 100},
            {"customer_id": "cus_2", "channel_id": "C2", "message_count": 5},
        ]
