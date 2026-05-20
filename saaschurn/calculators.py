def calculate_mrr(sub):
    """Calculate MRR for a subscription."""
    unit_amount = sub.get('plan', {}).get('unit_amount', 0)
    return unit_amount / 100  # Stripe uses cents


def calculate_churn_risk(mrr, activity_score):
    """Calculate churn risk score (0-100)."""
    base_score = 50
    if mrr < 1000:  # Example threshold
        base_score += 10
    if activity_score < 10:
        base_score += 20
    return min(base_score, 100)
