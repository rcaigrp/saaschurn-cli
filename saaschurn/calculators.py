def calculate_churn_risk(mrr, previous_mrr, slack_activity):
    """Calculate churn risk score based on MRR decline and Slack activity."""
    score = 50
    if previous_mrr > 0 and mrr < previous_mrr * 0.95:
        score -= 10
    if slack_activity < 10:
        score += 20
    score = max(0, min(100, score))
    risk_level = "LOW" if score < 30 else "MEDIUM" if score <= 70 else "HIGH"
    recommendation = "Monitor closely" if risk_level == "HIGH" else "Healthy" if risk_level == "LOW" else "Review engagement"
    return {"score": score, "level": risk_level, "recommendation": recommendation}
