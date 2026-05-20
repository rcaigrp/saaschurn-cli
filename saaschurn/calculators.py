def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        if sub.get("status") == "active":
            mrr += sub.get("plan", {}).get("amount", 0) / 100
    return mrr

def calculate_churn_risk(mrr, activity_score):
    score = 50
    if mrr < 1000:
        score -= 20
    if activity_score < 10:
        score += 30
    return max(0, min(100, score))

def get_risk_level(score):
    if score < 30:
        return "LOW"
    elif score < 70:
        return "MEDIUM"
    else:
        return "HIGH"
