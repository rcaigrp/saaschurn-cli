import os
import requests
import time

def fetch_stripe_data():
    api_key = os.getenv('STRIPE_API_KEY')
    if not api_key:
        raise ValueError("STRIPE_API_KEY not set")
    
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    subscriptions = []
    params = {"status": "active"}
    next_url = url
    while next_url:
        resp = requests.get(next_url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        for sub in data.get("data", []):
            subscriptions.append({
                "id": sub.get("customer"),
                "mrr": sub.get("plan", {}).get("amount") / 100,
                "status": sub.get("status")
            })
        next_url = data.get("next_url")
        time.sleep(1) 
    return subscriptions

def fetch_slack_data():
    slack_token = os.getenv('SLACK_API_TOKEN')
    if not slack_token:
        raise ValueError("SLACK_API_TOKEN not set")
    return {}
