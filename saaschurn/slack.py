import requests

def fetch_channel_activity(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get("https://slack.com/api/conversations.history", headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        return data.get("messages", [])
    return []
