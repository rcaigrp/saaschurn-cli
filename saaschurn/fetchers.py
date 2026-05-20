import requests
import os
import time

def fetch_stripe_subscriptions(api_key=None):
    if not api_key:
        api_key = os.getenv('STRIPE_API_KEY')
    if not api_key:
        raise ValueError("STRIPE_API_KEY environment variable not set")
    
    headers = {"Authorization": f"Bearer {api_key}"}
    url = "https://api.stripe.com/v1/subscriptions"
    params = {"limit": 100}
    
    subscriptions = []
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 429:
                time.sleep(5)
                continue
            response.raise_for_status()
            data = response.json()
            subscriptions.extend(data.get('data', []))
            if not data.get('has_more'):
                break
            params['starting_after'] = data.get('data')[-1].get('id')
        except Exception:
            raise
    return subscriptions

def fetch_slack_activity(slack_token=None, channels=None):
    if not slack_token:
        slack_token = os.getenv('SLACK_API_TOKEN')
    if not slack_token:
        raise ValueError("SLACK_API_TOKEN environment variable not set")
    if not channels:
        channels = []
        
    headers = {"Authorization": f"Bearer {slack_token}"}
    url = "https://slack.com/api/conversations.history"
    
    activity = {}
    for channel in channels:
        params = {"channel": channel, "limit": 100}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 429:
                time.sleep(5)
                continue
            response.raise_for_status()
            data = response.json()
            messages = data.get('messages', [])
            activity[channel] = len(messages)
        except Exception:
            activity[channel] = 0
    return activity
