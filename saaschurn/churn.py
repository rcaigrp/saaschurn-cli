import os
import stripe
from slack_sdk import WebClient

def run_health_check(dry_run=False):
    stripe.api_key = os.environ.get('STRIPE_API_TOKEN')
    slack_token = os.environ.get('SLACK_API_TOKEN')
    
    if dry_run:
        return {"status": "simulated", "mrr": 0, "churn_probability": 0.0}
    
    subs = stripe.Subscription.list(limit=100)
    mrr = sum(sub.get('plan', {}).get('amount', 0) / 100 for sub in subs.data)
    
    client = WebClient(token=slack_token)
    channels = client.conversations.list()
    
    return {"mrr": mrr, "status": "active", "churn_probability": 0.1}
