import requests

def fetch_subscriptions(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get("https://api.stripe.com/v1/subscriptions", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("data", [])
    return []
