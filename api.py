import stripe
from slack_sdk.web import WebClient

def fetch_data(api_key, slack_token=None):
    stripe.api_key = api_key
    subscriptions = stripe.Subscription.list().data
    total_mrr = sum(sub["plan"]["amount"] for sub in subscriptions) / 100
    recent_messages = 0
    if slack_token:
        client = WebClient(token=slack_token)
        response = client.conversations_history(channel="general")
        recent_messages = len(response.get("messages", []))
    return total_mrr, recent_messages
