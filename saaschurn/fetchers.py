import requests
import os

def fetch_stripe_subscriptions(token=None, url="https://api.stripe.com/v1/subscriptions"):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def fetch_slack_activity(token=None, url="https://slack.com/api/conversations.history"):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()
