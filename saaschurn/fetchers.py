"""API wrappers for Stripe and Slack."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


class StripeFetcher:
    def __init__(self):
        self.api_key = os.getenv('STRIPE_API_KEY')
        if not self.api_key:
            raise ValueError("STRIPE_API_KEY not set")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    def get_active_subscriptions(self):
        url = "https://api.stripe.com/v1/subscriptions"
        params = {"status": "active"}
        all_subs = []
        while True:
            resp = requests.get(url, headers=self.headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            all_subs.extend(data.get('data', []))
            if not data.get('has_more', False):
                break
            params['starting_after'] = data['last_object_id']
        return all_subs

    def get_mock_subscriptions(self):
        return [
            {"id": "sub_1", "customer": "cus_1", "status": "active", "plan": {"unit_amount": 1000, "currency": "usd"}},
            {"id": "sub_2", "customer": "cus_2", "status": "active", "plan": {"unit_amount": 2000, "currency": "usd"}},
        ]


class SlackFetcher:
    def __init__(self):
        self.token = os.getenv('SLACK_API_TOKEN')
        if not self.token:
            raise ValueError("SLACK_API_TOKEN not set")
    
    def get_channel_activity(self):
        url = "https://slack.com/api/conversations.history"
        headers = {"Authorization": f"Bearer {self.token}"}
        # Mock logic for aggregation
        return []

    def get_mock_activity(self):
        return [
            {"channel": "channel_1", "messages": 100},
            {"channel": "channel_2", "messages": 5},
        ]
