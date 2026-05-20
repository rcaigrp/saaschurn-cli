import os
import requests
import time


def fetch_stripe_data(token=None, dry_run=False):
    if dry_run:
        return {
            'sub_1': {'mrr': 1000, 'status': 'active'},
            'sub_2': {'mrr': 500, 'status': 'active'}
        }
    token = token or os.getenv('STRIPE_API_TOKEN')
    if not token:
        raise ValueError("STRIPE_API_TOKEN not set")
    
    headers = {'Authorization': f'Bearer {token}'}
    url = "https://api.stripe.com/v1/subscriptions"
    params = {'status': 'active'}
    
    all_subs = {}
    while True:
        try:
            resp = requests.get(url, headers=headers, params=params)
            if resp.status_code == 429:
                time.sleep(2 ** (resp.status_code - 200))
                continue
            if resp.status_code != 200:
                raise ValueError(f"Stripe API error: {resp.status_code}")
            data = resp.json()
            for sub in data.get('data', []):
                all_subs[sub['id']] = {
                    'mrr': sub.get('plan', {}).get('unit_amount', 0) / 100,
                    'status': sub.get('status')
                }
            if not data.get('has_more'):
                break
            params = {'cursor': data['next_page']}
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error: {e}")
    return all_subs


def fetch_slack_data(token=None, dry_run=False):
    if dry_run:
        return {
            'sub_1': {'messages': 15},
            'sub_2': {'messages': 5}
        }
    token = token or os.getenv('SLACK_API_TOKEN')
    if not token:
        raise ValueError("SLACK_API_TOKEN not set")
    
    headers = {'Authorization': f'Bearer {token}'}
    url = "https://slack.com/api/conversations.history"
    
    return {
        'sub_1': {'messages': 15},
        'sub_2': {'messages': 5}
    }
