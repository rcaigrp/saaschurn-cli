import os
import requests
import time


def fetch_stripe_subscriptions(token):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 100}
    all_subs = []

    # Pagination
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_subs.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            cursor = data.get("next_cursor")
            if cursor:
                params["starting_after"] = cursor
            else:
                break

        except requests.exceptions.HTTPError as e:
            print(f"Stripe API Error: {e}")
            break

        # Rate limit handling (429)
        if response.status_code == 429:
            print("Stripe rate limited. Sleeping...")
            time.sleep(2 ** (2 - 1))
            continue

    return all_subs


def fetch_slack_activity(token, client_channels):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    activity = {}

    for channel_id in client_channels:
        params = {"channel": channel_id, "limit": 100, "inclusive": "true"}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            messages = data.get("messages", [])
            # Filter last 30 days
            cutoff = time.time() - (30 * 24 * 60 * 60)
            count = sum(1 for m in messages if float(m.get("ts", 0)) > cutoff)
            activity[channel_id] = count
        except requests.exceptions.HTTPError as e:
            print(f"Slack API Error: {e}")
            continue

    return activity
