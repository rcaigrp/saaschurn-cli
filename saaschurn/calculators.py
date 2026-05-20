def calculate_churn_risk(mrr, slack_activity):
    base_score = 50
    score = base_score
    if mrr < 1000:
        score -= 10
    if mrr > 5000:
        score += 10
    if slack_activity < 10:
        score += 20
    if slack_activity > 50:
        score -= 10
    return max(0, min(100, score))

def get_risk_level(score):
    if score < 30:
        return "LOW"
    elif score <= 70:
        return "MEDIUM"
    else:
        return "HIGH"

def get_recommendation(risk_level):
    if risk_level == "HIGH":
        return "Immediate outreach required"
    elif risk_level == "MEDIUM":
        return "Schedule check-in"
    else:
        return "No action needed"
