import requests
import time

def fetch_stripe_data(token):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"status": "active"}
    subscriptions = []
    
    while True:
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            subscriptions.extend(data.get("data", []))
            if not data.get("has_more"):
                break
            params["starting_after"] = data.get("last_cursor")
            time.sleep(0.5)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(5)
                continue
            raise
    return subscriptions

def fetch_slack_data(token, client_names):
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    activity = {}
    
    for client in client_names:
        channel = f"#{client.lower().replace(' ', '-')}"
        params = {"channel": channel}
        try:
            resp = requests.get(url, headers=headers, params=params)
            resp.raise_for_status()
            data = resp.json()
            msgs = len(data.get("messages", []))
            activity[client] = {"messages_count": msgs}
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                time.sleep(5)
                continue
            activity[client] = {"messages_count": 0}
    return activity
