import os
import stripe
import responses
from typing import List, Dict, Any


def fetch_subscriptions() -> List[Dict[str, Any]]:
    stripe.api_key = os.environ.get('STRIPE_API_TOKEN')
    subscriptions = stripe.Subscription.list(limit=100)
    active = []
    for sub in subscriptions.data:
        if sub.status == 'active':
            active.append({
                'id': sub.id,
                'customer_id': sub.customer,
                'plan': sub.items.data[0].plan.nickname if sub.items.data else 'Unknown',
                'mrr': sub.items.data[0].plan.amount / 100 if sub.items.data else 0,
                'created': sub.created
            })
    return active


def fetch_slack_activity() -> List[Dict[str, Any]]:
    from slack_sdk import WebClient
    client = WebClient(token=os.environ.get('SLACK_API_TOKEN'))
    channels = client.conversations_list()
    activity = []
    for channel in channels.get('channels', []):
        if channel.get('name', '').startswith('client-'):
            messages = client.conversations_history(channel=channel['id'], limit=50)
            messages_list = messages.get('messages', [])
            activity.append({
                'channel': channel['name'],
                'message_count': len(messages_list),
                'last_message': messages_list[-1].get('text', '') if messages_list else ''
            })
    return activity
