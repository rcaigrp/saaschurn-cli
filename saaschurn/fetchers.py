import os
import requests
import time


def fetch_stripe_subscriptions(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.stripe.com/v1/subscriptions"
    all_subs = []
    params = {"status": "active"}
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            all_subs.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            params["starting_after"] = data.get("next_cursor")
            time.sleep(0.1)
        except requests.HTTPError as e:
            print(f"Stripe API Error: {e}")
            break
    return all_subs


def fetch_slack_activity(token, channel_id):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://slack.com/api/conversations.history"
    params = {"channel": channel_id, "limit": 100}
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("messages", [])
    except requests.HTTPError as e:
        print(f"Slack API Error: {e}")
        return []
