import stripe

def fetch_active_subscriptions(api_key):
    stripe.api_key = api_key
    subscriptions = stripe.Subscription.list(status='active')
    return subscriptions.data

def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        mrr += sub['plan']['amount'] / 100
    return mrr
