def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        plan = sub.get('plan', {})
        amount = plan.get('amount', 0) / 100
        mrr += amount
    return mrr

def calculate_churn_risk(mrr, activity_score):
    risk = 50
    if mrr < 1000:
        risk += 20
    if activity_score < 10:
        risk += 30
    if risk > 100: risk = 100
    if risk < 0: risk = 0
    return risk

def get_risk_level(risk):
    if risk < 30: return "LOW"
    if risk <= 70: return "MEDIUM"
    return "HIGH"