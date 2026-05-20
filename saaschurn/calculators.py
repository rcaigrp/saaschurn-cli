def calculate_mrr(plan_amount_cents):
    return plan_amount_cents / 100

def calculate_churn_risk(mrr_decline_pct, slack_activity_pct):
    base = 50
    if mrr_decline_pct > 5:
        base -= 10
    if slack_activity_pct < 10:
        base += 20
    return max(0, min(100, base))

def get_risk_level(score):
    if score < 30:
        return "LOW"
    elif score <= 70:
        return "MEDIUM"
    else:
        return "HIGH"

def get_recommendation(level):
    if level == "LOW":
        return "Healthy"
    elif level == "MEDIUM":
        return "Monitor"
    else:
        return "At Risk"
