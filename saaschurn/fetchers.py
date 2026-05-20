import requests
import os

def fetch_stripe_data(api_key):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"status": "active"}
    all_subs = []
    while True:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        for sub in data.get("data", []):
            mrr = sub.get("amount", 0) / 100
            all_subs.append({"id": sub.get("id"), "customer": sub.get("customer"), "mrr": mrr})
        if not data.get("has_more"):
            break
        params["starting_after"] = data.get("next_cursor")
    return all_subs

def fetch_slack_data(token, channels=None):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    results = {}
    if not channels:
        return results
    for ch in channels:
        params = {"channel": ch, "limit": 10}
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            messages = resp.json().get("messages", [])
            results[ch] = len(messages)
        except requests.exceptions.HTTPError:
            pass
    return results

def get_mock_stripe_data():
    return [{"id": "sub_1", "customer": "cust_1", "mrr": 100.0}, {"id": "sub_2", "customer": "cust_2", "mrr": 50.0}]

def get_mock_slack_data():
    return {"channel_1": 50, "channel_2": 5}
