import os
import time
import requests


def fetch_stripe_subscriptions(stripe_token):
    """Fetch active subscriptions from Stripe API."""
    headers = {"Authorization": f"Bearer {stripe_token}"}
    url = "https://api.stripe.com/v1/subscriptions"
    params = {"status": "active"}
    all_subs = []
    next_url = url
    while True:
        try:
            resp = requests.get(next_url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            if "data" in data:
                all_subs.extend(data["data"])
                if "next_page" in data:
                    next_url = data["next_page"]
                else:
                    break
            else:
                break
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(2 ** len(all_subs))
                continue
            raise
    return all_subs


def fetch_slack_activity(slack_token):
    """Fetch channel activity from Slack API."""
    headers = {"Authorization": f"Bearer {slack_token}"}
    url = "https://slack.com/api/conversations.history"
    channels = ["client-alpha", "client-beta", "client-gamma"]
    activity = {}
    for channel in channels:
        params = {"channel": channel, "count": 1000}
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            if "messages" in data:
                activity[channel] = len(data["messages"])
            else:
                activity[channel] = 0
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(2)
                continue
            activity[channel] = 0
    return activity
