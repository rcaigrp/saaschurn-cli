import os
import stripe
import slack_sdk
from datetime import datetime

def get_stripe_client():
    token = os.getenv('STRIPE_API_TOKEN')
    if not token:
        raise ValueError("STRIPE_API_TOKEN not set")
    stripe.api_key = token
    return stripe

def get_slack_client():
    token = os.getenv('SLACK_API_TOKEN')
    if not token:
        raise ValueError("SLACK_API_TOKEN not set")
    return slack_sdk.WebClient(token=token)

def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        if sub.get('status') == 'active':
            mrr += sub.get('plan', {}).get('amount', 0) / 100
    return mrr

def get_slack_activity(client, channel_ids):
    activity = {}
    for cid in channel_ids:
        response = client.conversations_history(channel=cid, limit=10)
        messages = response.get('messages', [])
        activity[cid] = len(messages)
    return activity

def compute_churn_score(mrr_history, activity_history):
    mrr_decline = 1 - (mrr_history[-1] / mrr_history[0]) if mrr_history[0] > 0 else 0
    activity_drop = 1 - (activity_history[-1] / activity_history[0]) if activity_history[0] > 0 else 0
    score = (mrr_decline * 0.6) + (activity_drop * 0.4)
    return round(score * 100, 2)
