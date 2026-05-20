def calculate_churn_risk(mrr, mrr_decline_pct, slack_activity_score):
    score = 50
    if mrr_decline_pct > 5:
        score -= (mrr_decline_pct - 5) * 2
    if slack_activity_score < 10:
        score += (10 - slack_activity_score) * 2
    score = max(0, min(100, score))
    if score < 30:
        risk_level = "LOW"
    elif score <= 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
    return score, risk_level
