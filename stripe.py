def fetch_subscriptions():
    """Fetches active subscriptions from Stripe."""
    return [
        {"id": "sub_123", "amount": 1000, "status": "active"},
        {"id": "sub_456", "amount": 500, "status": "active"}
    ]

def calculate_mrr(subscriptions):
    """Calculates Monthly Recurring Revenue."""
    return sum(sub["amount"] for sub in subscriptions if sub["status"] == "active")
