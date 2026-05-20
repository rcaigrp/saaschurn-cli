def calculate_mrr(subscriptions):
    total_mrr = 0
    for sub in subscriptions:
        # Assuming MRR is in the plan object
        if "plan" in sub and "amount" in sub["plan"]:
            total_mrr += sub["plan"]["amount"] / 100 # Stripe uses cents
    return total_mrr

def calculate_activity_score(msg_count):
    # Base score 50. Add points for activity.
    if msg_count > 100:
        return 80
    elif msg_count > 50:
        return 60
    else:
        return 30

def calculate_churn_risk(mrr, activity_score):
    # Logic: Base 50. Subtract for MRR decline? (Not tracked in simple fetch)
    # Add for low activity.
    risk = 50
    if activity_score < 50:
        risk += 30
    return min(risk, 100)
