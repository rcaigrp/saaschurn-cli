try:
    import stripe
except ImportError:
    stripe = None

def get_subscriptions(token):
    if stripe is None:
        return []
    stripe.api_key = token
    return stripe.Subscription.list(status='active').data
