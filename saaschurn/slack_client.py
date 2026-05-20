import requests

def fetch_channel_activity(token, channel_ids):
    headers = {'Authorization': f'Bearer {token}'}
    activity = {}
    for channel_id in channel_ids:
        url = "https://slack.com/api/conversations.history"
        params = {'channel': channel_id, 'limit': 10}
        response = requests.get(url, headers=headers, params=params)
        activity[channel_id] = response.json()
    return activity
