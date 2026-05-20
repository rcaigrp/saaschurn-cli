import requests

def get_channel_activity(token, channels):
    url = "https://api.slack.com/methods/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"channel": channels[0], "limit": 10}
    resp = requests.get(url, headers=headers, params=data)
    resp.raise_for_status()
    messages = resp.json().get("messages", [])
    return {
        "channel": channels[0],
        "message_count": len(messages),
        "last_message": messages[-1].get("text", "") if messages else ""
    }
