import requests

class SlackClient:
    def __init__(self, token):
        self.token = token
        self.api_url = 'https://slack.com/api/conversations.history'

    def get_workspace_activity(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'channel': 'general'}
        resp = requests.get(self.api_url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()['messages']
