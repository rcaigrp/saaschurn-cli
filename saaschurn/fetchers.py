import requests
import time

def fetch_stripe_subscriptions(token):
    headers = {"Authorization": f"Bearer {token}"}
    url = "https://api.stripe.com/v1/subscriptions"
    params = {"status": "active"}
    subscriptions = []
    while True:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Stripe API error: {response.status_code}")
        data = response.json()
        subscriptions.extend(data.get("data", []))
        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break
        params["starting_after"] = next_cursor
        time.sleep(0.1) # Rate limit handling
    return subscriptions

def fetch_slack_activity(token, channel_ids):
    headers = {"Authorization": f"Bearer {token}"}
    activity = {}
    for channel_id in channel_ids:
        url = "https://slack.com/api/conversations.history"
        params = {"channel": channel_id, "limit": 1000}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            messages = data.get("messages", [])
            activity[channel_id] = len(messages)
        else:
            activity[channel_id] = 0
    return activity
