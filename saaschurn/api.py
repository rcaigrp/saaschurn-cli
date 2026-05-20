import os
import requests

def fetch_subscriptions():
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {'Authorization': f"Bearer {os.getenv('STRIPE_API_TOKEN')}"}
    return requests.get(url, headers=headers).json()

def fetch_slack_activity(channel):
    url = f"https://slack.com/api/conversations.history?channel={channel}"
    headers = {'Authorization': f"Bearer {os.getenv('SLACK_API_TOKEN')}"}
    return requests.get(url, headers=headers).json().get('messages', [])
