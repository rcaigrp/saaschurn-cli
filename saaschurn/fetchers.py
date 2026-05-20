import requests


def fetch_stripe_data(token, dry_run=False):
    if dry_run:
        return [{"client": "Client A", "mrr": 1000}, {"client": "Client B", "mrr": 500}]
    
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"status": "active"}
    
    subscriptions = []
    next_cursor = None
    
    while True:
        if next_cursor:
            params["cursor"] = next_cursor
        
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        for sub in data.get("data", []):
            subscriptions.append({
                "client": sub.get("customer"),
                "mrr": sub.get("plan", {}).get("amount") / 100
            })
            
        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break
            
    return subscriptions


def fetch_slack_data(token, dry_run=False):
    if dry_run:
        return [{"client": "Client A", "score": 80}]
    
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"channel": "general", "limit": 100}
    
    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    
    return [{"client": "Client A", "score": len(data.get("messages", []))}]