import requests
import time

def fetch_stripe(token, dry_run=False):
    if dry_run:
        return [
            {"id": "sub_1", "customer_id": "cus_A", "customer_name": "ClientA", "status": "active", "quantity": 1, "plan": {"amount": 10000}},
            {"id": "sub_2", "customer_id": "cus_B", "customer_name": "ClientB", "status": "active", "quantity": 2, "plan": {"amount": 5000}},
        ]
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    subscriptions = []
    while True:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        subscriptions.extend(data.get("data", []))
        if not data.get("has_more"):
            break
        time.sleep(1) 
        url = data["url"]
    return subscriptions

def fetch_slack(token, dry_run=False):
    if dry_run:
        return {"ClientA": 15, "ClientB": 5}
    url = "https://slack.com/api/conversations.list"
    headers = {"Authorization": f"Bearer {token}"}
    channels = []
    while True:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        channels.extend([c for c in data.get("channels", []) if c.get("is_channel")])
        if not data.get("response_metadata", {}).get("next_cursor"):
            break
        time.sleep(1)
        url = f"https://slack.com/api/conversations.list?cursor={data['response_metadata']['next_cursor']}"
    
    activity = {}
    for ch in channels:
        name = ch.get("name")
        if name not in activity:
            activity[name] = 0
        hist_url = f"https://slack.com/api/conversations.history?channel={ch['id']}&limit=100"
        hist_resp = requests.get(hist_url, headers=headers)
        hist_resp.raise_for_status()
        hist_data = hist_resp.json()
        activity[name] += len(hist_data.get("messages", []))
    return activity
