import requests
import os
import time

STRIPE_API_URL = "https://api.stripe.com/v1/subscriptions"
SLACK_API_URL = "https://slack.com/api/conversations.history"

def fetch_stripe_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    all_subs = []
    url = STRIPE_API_URL
    while True:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Stripe API error: {response.status_code}")
                break
            data = response.json()
            all_subs.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            url = data.get("next_page_url") or data.get("next_cursor")
        except requests.exceptions.RequestException as e:
            print(f"Stripe request failed: {e}")
            break
    return {"subscriptions": all_subs}

def fetch_slack_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    all_channels = []
    url = SLACK_API_URL
    while True:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Slack API error: {response.status_code}")
                break
            data = response.json()
            # Aggregate messages by channel
            for msg in data.get("messages", []):
                channel_name = msg.get("channel")
                if channel_name and not any(c.get("name") == channel_name for c in all_channels):
                    all_channels.append({"name": channel_name, "messages": 0})
                for ch in all_channels:
                    if ch.get("name") == channel_name:
                        ch["messages"] += 1
                        break
            if not data.get("has_more"):
                break
            url = data.get("next_cursor")
        except requests.exceptions.RequestException as e:
            print(f"Slack request failed: {e}")
            break
    return {"channels": all_channels}
