import os
import requests

def fetch_active_subscriptions(token):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"status": "active"}
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json().get("data", [])
    except requests.exceptions.RequestException:
        return []

def calc_mrr(subscriptions):
    total = 0
    for sub in subscriptions:
        plan = sub.get("plan", {})
        amount = plan.get("amount", 0)
        total += amount / 100
    return total
