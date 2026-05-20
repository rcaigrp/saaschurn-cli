def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        if sub.get("status") == "active":
            mrr += sub.get("plan", {}).get("amount", 0) / 100  # Stripe amounts in cents
    return mrr

def calculate_churn_risk(mrr, slack_activity_score):
    base_score = 50
    if mrr < 0.05:  # Placeholder for decline logic
        base_score += 20
    if slack_activity_score < 10:
        base_score += 30
    return base_score
