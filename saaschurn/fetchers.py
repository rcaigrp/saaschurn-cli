import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_subscriptions():
    stripe_key = os.getenv('STRIPE_API_KEY')
    if not stripe_key:
        raise ValueError('STRIPE_API_KEY not found in environment')
    
    url = 'https://api.stripe.com/v1/subscriptions'
    headers = {'Authorization': f'Bearer {stripe_key}'}
    subs = {}
    next_url = url
    
    while True:
        try:
            resp = requests.get(next_url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching subscriptions: {e}")
            break
            
        for sub in data.get('data', []):
            if sub.get('status') == 'active':
                cid = sub.get('customer')
                if cid:
                    plan = sub.get('plan', {})
                    amount = plan.get('amount', 0)
                    qty = sub.get('quantity', 1)
                    mrr = (amount * qty) / 100
                    if cid not in subs:
                        subs[cid] = mrr
                    else:
                        subs[cid] += mrr
            
        if not data.get('has_more'):
            break
        next_url = data.get('next_url')
        if not next_url:
            break
            
    return subs

def fetch_slack_activity():
    token = os.getenv('SLACK_API_TOKEN')
    if not token:
        raise ValueError('SLACK_API_TOKEN not found in environment')
    
    url = 'https://slack.com/api/conversations.history'
    headers = {'Authorization': f'Bearer {token}'}
    
    list_url = 'https://slack.com/api/conversations.list'
    list_headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(list_url, headers=list_headers)
    resp.raise_for_status()
    channels = resp.json().get('channels', [])
    
    activity = {}
    for ch in channels:
        cid = ch.get('id')
        if cid:
            hist_url = f"{url}?channel={cid}&limit=100"
            resp = requests.get(hist_url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                count = len(data.get('messages', []))
                activity[cid] = count
            else:
                print(f"Error fetching history for channel {cid}: {resp.status_code}")
                
    return activity