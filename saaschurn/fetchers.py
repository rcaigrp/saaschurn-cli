import os
import time
import requests
from typing import List, Dict, Optional


class StripeFetcher:
    """Fetches active subscriptions from Stripe API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.stripe.com/v1/subscriptions"

    def fetch_active_subscriptions(self) -> List[Dict]:
        """Fetch all active subscriptions with pagination and rate limit handling."""
        subscriptions = []
        url = self.base_url

        while True:
            try:
                response = requests.get(
                    url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    params={"status": "active"}
                )

                # Handle rate limits with exponential backoff
                if response.status_code == 429:
                    wait_time = min(2 ** len(subscriptions), 60)
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()

                for sub in data.get("data", []):
                    subscriptions.append(sub)

                if data.get("has_more"):
                    url = data.get("next_page_url", f"{self.base_url}?page_token={data.get('next_page_token')}")
                else:
                    break

            except requests.exceptions.RequestException as e:
                raise Exception(f"Request error: {e}")

        return subscriptions

    def calculate_mrr(self, subscriptions: List[Dict]) -> Dict[str, float]:
        """Calculate MRR per client from subscriptions."""
        mrr_data = {}
        for sub in subscriptions:
            customer_id = sub.get("customer", "")
            price_info = sub.get("plan", {})
            if price_info and "amount" in price_info:
                mrr = price_info["amount"] / 100  # Stripe returns in cents
                mrr_data[customer_id] = mrr
        return mrr_data


class SlackFetcher:
    """Fetches channel activity from Slack API."""

    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://slack.com/api/conversations.history"

    def fetch_channel_activity(self, channels: List[str]) -> Dict[str, int]:
        """Fetch message counts for given channels."""
        activity = {}
        for channel in channels:
            try:
                response = requests.get(
                    self.base_url,
                    headers={"Authorization": f"Bearer {self.token}"},
                    params={"channel": channel, "limit": 100}
                )
                if response.status_code == 429:
                    time.sleep(60)
                    continue
                response.raise_for_status()
                data = response.json()
                messages = data.get("messages", [])
                activity[channel] = len(messages)
            except requests.exceptions.RequestException:
                activity[channel] = 0
        return activity
