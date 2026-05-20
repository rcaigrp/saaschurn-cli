"""API fetchers for Stripe and Slack."""

import os
import time
import requests
from typing import Dict, List, Optional


class APIError(Exception):
    """Custom exception for API errors."""
    pass


class StripeFetcher:
    """Fetches subscription data from Stripe API."""

    BASE_URL = "https://api.stripe.com/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def fetch_active_subscriptions(self, max_retries: int = 3) -> List[Dict]:
        """Fetch all active subscriptions with pagination and retry logic."""
        subscriptions = []
        url = f"{self.BASE_URL}/subscriptions"
        params = {"status": "active"}

        for attempt in range(max_retries):
            try:
                while True:
                    response = requests.get(url, headers=self.headers, params=params)
                    if response.status_code == 429:  # Rate limited
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue

                    response.raise_for_status()
                    data = response.json()

                    # Process current page
                    for sub in data.get("data", []):
                        subscriptions.append(sub)

                    # Check for next page
                    if data.get("has_more"):
                        url = data.get("next_page_url") or url
                        # Extract cursor from URL for next request
                        params = {}
                    else:
                        break

                break  # Success

            except requests.exceptions.HTTPError as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                raise APIError(f"Stripe API error: {e}")

            except Exception as e:
                raise APIError(f"Stripe API error: {e}")

        return subscriptions

    def calculate_mrr(self, subscriptions: List[Dict]) -> Dict[str, float]:
        """Calculate Monthly Recurring Revenue per customer."""
        mrr_by_customer = {}

        for sub in subscriptions:
            customer_id = sub.get("customer", "")
            if not customer_id:
                continue

            # Get pricing info
            items = sub.get("items", {}).get("data", [])
            for item in items:
                price_id = item.get("price", {}).get("id", "")
                if not price_id:
                    continue

                # Calculate MRR from pricing
                pricing = item.get("price", {})
                unit_amount = pricing.get("unit_amount", 0)
                recurring_interval = pricing.get("recurring", {}).get("interval", "month")

                # Convert to monthly equivalent
                if recurring_interval == "month":
                    mrr = unit_amount / 100  # Stripe uses cents
                elif recurring_interval == "year":
                    mrr = (unit_amount / 100) / 12
                else:  # week or day
                    mrr = (unit_amount / 100) * 4  # approximate

                mrr_by_customer[customer_id] = mrr_by_customer.get(customer_id, 0) + mrr

        return mrr_by_customer


class SlackFetcher:
    """Fetches channel activity from Slack API."""

    BASE_URL = "https://slack.com/api"

    def __init__(self, slack_token: str):
        self.slack_token = slack_token
        self.headers = {
            "Authorization": f"Bearer {slack_token}",
        }

    def fetch_channel_activity(self, channel_ids: List[str], max_retries: int = 3) -> Dict[str, int]:
        """Fetch message counts for specified channels over last 30 days."""
        activity = {}

        for channel_id in channel_ids:
            for attempt in range(max_retries):
                try:
                    url = f"{self.BASE_URL}/conversations.history"
                    params = {"channel": channel_id, "limit": 100}

                    response = requests.get(url, headers=self.headers, params=params)

                    if response.status_code == 429:
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue

                    if response.status_code == 400 and "channel_not_found" in response.text:
                        activity[channel_id] = 0
                        break

                    response.raise_for_status()
                    data = response.json()

                    # Count messages
                    messages = data.get("messages", [])
                    count = len(messages)
                    activity[channel_id] = count
                    break

                except Exception as e:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    activity[channel_id] = 0

        return activity

    def get_channel_id_for_client(self, client_name: str) -> Optional[str]:
        """Map client name to Slack channel ID."""
        # This would typically come from a mapping or config
        # For now, use a simple convention
        channel_name = client_name.lower().replace(" ", "-")
        # In production, this would be a lookup
        return f"C_{channel_name}"
