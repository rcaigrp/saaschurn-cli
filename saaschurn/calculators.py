def calculate_churn_risk(mrr, mrr_prev, slack_msgs):
    """Calculate churn risk score (0-100)."""
    score = 50
    if mrr_prev and mrr > 0:
        decline = (mrr_prev - mrr) / mrr_prev
        if decline > 0.05:
            score -= 10
    if slack_msgs < 10:
        score += 10
    return max(0, min(100, score))

def get_recommendation(risk):
    if risk < 30:
        return "Healthy"
    elif risk <= 70:
        return "Monitor closely"
    else:
        return "Immediate intervention required"
