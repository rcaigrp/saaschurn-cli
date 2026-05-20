import requests
import os

def fetch_stripe_data():
    api_key = os.getenv('STRIPE_API_KEY')
    if not api_key:
        raise ValueError("STRIPE_API_KEY not set")
    headers = {'Authorization': f'Bearer {api_key}'}
    url = "https://api.stripe.com/v1/subscriptions"
    params = {'status': 'active'}
    data = []
    next_url = url
    while next_url:
        resp = requests.get(next_url, headers=headers, params=params)
        resp.raise_for_status()
        resp_data = resp.json()
        data.extend(resp_data.get('data', []))
        next_url = resp_data.get('next_url')
    return data

def fetch_slack_data():
    token = os.getenv('SLACK_API_TOKEN')
    if not token:
        raise ValueError("SLACK_API_TOKEN not set")
    return []
