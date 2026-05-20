import os
import stripe
from slack_sdk.web import SlackClient

def run_health_check():
    stripe.api_key = os.getenv("STRIPE_API_TOKEN")
    slack_token = os.getenv("SLACK_API_TOKEN")
    
    subscriptions = stripe.Subscription.list(limit=10, status="active")
    mrr = sum(sub.total_amount_due or 0 for sub in subscriptions.data)
    
    client = SlackClient(slack_token)
    channels = client.conversations.list()
    history = client.conversations.history(channel=channels.data[0]["id"], limit=5) if channels.data else []
    activity_count = len(history)
    
    churn_score = 0.0
    if mrr < 1000:
        churn_score += 0.3
    if activity_count < 5:
        churn_score += 0.4
    
    return {
        "mrr": mrr,
        "activity_count": activity_count,
        "churn_probability": churn_score,
        "subscriptions_count": len(subscriptions.data)
    }
