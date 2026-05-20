import requests
import time
import os

def fetch_stripe_subscriptions(token):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 100}
    subscriptions = []
    page = 0
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 429:
                wait_time = 2 ** page
                time.sleep(wait_time)
                page += 1
                continue
            response.raise_for_status()
            data = response.json()
            subscriptions.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            params["starting_after"] = data.get("last_cursor")
            page += 1
        except Exception as e:
            print(f"Error fetching Stripe: {e}")
            break
    return subscriptions

def fetch_slack_activity(token, channel_ids):
    url = "https://api.slack.com/methods/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    activity = {}
    for cid in channel_ids:
        params = {"channel": cid}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 429:
                time.sleep(2)
                continue
            response.raise_for_status()
            data = response.json()
            activity[cid] = len(data.get("messages", []))
        except Exception as e:
            print(f"Error fetching Slack for {cid}: {e}")
            activity[cid] = 0
    return activity
