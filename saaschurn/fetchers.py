import os
import requests
import time

def fetch_stripe_subscriptions():
    stripe_key = os.getenv("STRIPE_API_KEY")
    if not stripe_key:
        raise ValueError("STRIPE_API_KEY not set")
    headers = {"Authorization": f"Bearer {stripe_key}"}
    url = "https://api.stripe.com/v1/subscriptions"
    subscriptions = []
    while True:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 429:
            time.sleep(2 ** len(subscriptions))
            continue
        data = resp.json()
        subscriptions.extend(data.get("data", []))
        if not data.get("has_more"):
            break
        url = data.get("next_page")
    return subscriptions

def calculate_mrr(subscriptions):
    mrr_map = {}
    for sub in subscriptions:
        client_id = sub.get("customer")
        price = sub.get("plan", {}).get("amount") or sub.get("price", {}).get("amount")
        if client_id:
            mrr_map[client_id] = mrr_map.get(client_id, 0) + (price / 100)
    return mrr_map

def fetch_slack_activity(channel_ids):
    slack_token = os.getenv("SLACK_API_TOKEN")
    if not slack_token:
        raise ValueError("SLACK_API_TOKEN not set")
    headers = {"Authorization": f"Bearer {slack_token}"}
    activity = {}
    for cid in channel_ids:
        url = "https://slack.com/api/conversations.history"
        params = {"channel": cid, "limit": 100}
        resp = requests.post(url, headers=headers, json=params)
        if resp.status_code == 200:
            data = resp.json()
            msgs = len(data.get("messages", []))
            activity[cid] = msgs
    return activity
