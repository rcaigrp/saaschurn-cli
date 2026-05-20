import requests

class SlackClient:
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://slack.com/api"

    def get_channel_history(self, channel_id):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        params = {"channel": channel_id}
        try:
            resp = requests.get(f"{self.base_url}/conversations.history", headers=headers, params=params)
            resp.raise_for_status()
            return resp.json().get("messages", [])
        except Exception:
            return []
