import os

def fetch_subscriptions(dry_run=False):
    if dry_run:
        return [{"client": "Acme Corp", "mrr": 500}]
    
    api_token = os.environ.get("STRIPE_API_TOKEN")
    if not api_token:
        raise ValueError("Missing STRIPE_API_TOKEN")
    return [{"client": "Stripe Client", "mrr": 1000}]

def fetch_slack_activity(dry_run=False):
    if dry_run:
        return {"channels": []}
    
    api_token = os.environ.get("SLACK_API_TOKEN")
    if not api_token:
        raise ValueError("Missing SLACK_API_TOKEN")
    return {"channels": []}
