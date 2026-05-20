import requests
import os
from dotenv import load_dotenv


def fetch_stripe_subscriptions(stripe_token=None, url=None):
    """Fetch active subscriptions from Stripe."""
    if not stripe_token:
        stripe_token = os.getenv('STRIPE_API_KEY')
    if not url:
        url = "https://api.stripe.com/v1/subscriptions"

    headers = {"Authorization": f"Bearer {stripe_token}"}
    subs = []
    params = {"limit": 100}

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        subs.extend(data.get('data', []))

        if not data.get('next'):
            break
        params['starting_after'] = data['next']

    return subs


def fetch_slack_activity(slack_token=None, url=None):
    """Fetch Slack channel activity."""
    if not slack_token:
        slack_token = os.getenv('SLACK_API_KEY')
    if not url:
        url = "https://slack.com/api/conversations.history"

    headers = {"Authorization": f"Bearer {slack_token}"}
    params = {"channel": "test", "limit": 100}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    # Simplified for demo: return mock structure
    return {"channels": response.json().get('messages', [])}
