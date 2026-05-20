import requests
import time
import os

def fetch_stripe_subscriptions(stripe_token):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {stripe_token}"}
    params = {"status": "active"}
    all_subscriptions = []
    
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 429:
                time.sleep(2)
                continue
            if response.status_code != 200:
                raise Exception(f"Stripe API error: {response.status_code}")
            
            data = response.json()
            all_subscriptions.extend(data.get('data', []))
            if not data.get('has_more'):
                break
            params['starting_after'] = data.get('last_cursor')
        except Exception as e:
            raise e
    return all_subscriptions

def fetch_slack_activity(slack_token, channel_ids=None):
    if channel_ids is None:
        channels_url = "https://slack.com/api/conversations.list"
        headers = {"Authorization": f"Bearer {slack_token}"}
        params = {"type": "private"}
        all_channels = []
        cursor = None
        
        while True:
            try:
                resp = requests.get(channels_url, headers=headers, params={'cursor': cursor} if cursor else {'type': 'private'})
                if resp.status_code == 429:
                    time.sleep(2)
                    continue
                data = resp.json()
                all_channels.extend([c['id'] for c in data.get('channels', [])])
                if not data.get('response_metadata', {}).get('next_cursor'):
                    break
                cursor = data['response_metadata']['next_cursor']
            except Exception:
                break
                
        channel_ids = all_channels
        
    activity = {}
    for cid in channel_ids:
        url = "https://slack.com/api/conversations.history"
        headers = {"Authorization": f"Bearer {slack_token}"}
        params = {"channel": cid}
        try:
            resp = requests.get(url, headers=headers, params=params)
            if resp.status_code == 429:
                time.sleep(2)
                continue
            if resp.status_code != 200:
                continue
            data = resp.json()
            messages = data.get('messages', [])
            count = len(messages)
            activity[cid] = count
        except Exception:
            continue
    return activity