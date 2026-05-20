def calculate_mrr(subscription):
    try:
        return float(subscription.get("plan", {}).get("amount", 0)) / 100
    except Exception:
        return 0.0

def calculate_churn_risk(mrr, activity_score):
    base_score = 50
    if mrr < 1000:
        base_score -= 10
    if activity_score < 10:
        base_score += 20
    elif activity_score < 50:
        base_score += 10
    return min(100, max(0, base_score))

def get_risk_level(score):
    if score < 30:
        return "LOW"
    elif score <= 70:
        return "MEDIUM"
    else:
        return "HIGH"