"""API fetchers for Stripe and Slack."""
import time
import os

import requests


class APIError(Exception):
    """Exception for API errors."""
    pass


class RateLimitError(APIError):
    """Exception for rate limit errors."""
    pass


class StripeFetcher:
    """Fetches subscription data from Stripe API."""

    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.stripe.com/v1/subscriptions"

    def get_active_subscriptions(self):
        """Fetch all active subscriptions from Stripe."""
        subscriptions = []
        url = self.base_url
        has_more = True

        while has_more:
            # Exponential backoff for rate limits
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, headers={"Authorization": f"Bearer {self.api_token}"})
                    if response.status_code == 429:
                        # Rate limited - exponential backoff
                        wait_time = 2 ** attempt
                        print(f"Rate limited. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    elif response.status_code != 200:
                        raise APIError(f"Stripe API error: {response.status_code}")
                    break
                except requests.exceptions.RequestException as e:
                    raise APIError(f"Network error: {e}")

            data = response.json()
            subscriptions.extend(data.get("data", []))
            has_more = data.get("has_more", False)
            if has_more:
                url = data.get("next_page_url", "")

        return subscriptions


class SlackFetcher:
    """Fetches channel activity from Slack API."""

    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://slack.com/api/conversations.history"

    def get_channel_activity(self):
        """Fetch channel activity for all client channels."""
        channels = []

        # Get all channels
        channel_list_url = "https://slack.com/api/conversations.list"
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    channel_list_url,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                    params={"limit": 100}
                )
                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                elif response.status_code != 200:
                    raise APIError(f"Slack API error: {response.status_code}")
                break
            except requests.exceptions.RequestException as e:
                raise APIError(f"Network error: {e}")

        channel_data = response.json()
        channels = channel_data.get("channels", [])

        # Fetch message history for each channel
        channel_activities = []
        for channel in channels:
            channel_name = channel.get("name", "")
            channel_id = channel.get("id", "")

            # Check if this is a client channel (simple heuristic)
            if "client" in channel_name.lower() or "support" in channel_name.lower():
                # Fetch message history
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = requests.get(
                            self.base_url,
                            headers={"Authorization": f"Bearer {self.api_token}"},
                            params={"channel": channel_id, "limit": 100}
                        )
                        if response.status_code == 429:
                            wait_time = 2 ** attempt
                            print(f"Rate limited. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                            continue
                        elif response.status_code != 200:
                            raise APIError(f"Slack API error: {response.status_code}")
                        break
                    except requests.exceptions.RequestException as e:
                        raise APIError(f"Network error: {e}")

                history = response.json()
                messages = history.get("messages", [])

                # Count messages in last 30 days
                message_count = 0
                for message in messages:
                    # Simple heuristic: count all messages in the response
                    message_count += len(messages)
                    break  # Only count once for simplicity

                # Extract customer name from channel name
                customer_name = channel_name.replace("#", "").replace("-", " ").replace("_", " ").title()

                channel_activities.append({
                    "customer_name": customer_name,
                    "channel_name": channel_name,
                    "message_count": message_count
                })

        return channel_activities
