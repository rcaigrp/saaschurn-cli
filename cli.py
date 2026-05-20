import os

def get_config():
    stripe_token = os.environ.get("STRIPE_API_TOKEN")
    slack_token = os.environ.get("SLACK_API_TOKEN")
    if not stripe_token or not slack_token:
        raise ValueError("Missing API tokens")
    return {
        "stripe_token": stripe_token,
        "slack_token": slack_token
    }
