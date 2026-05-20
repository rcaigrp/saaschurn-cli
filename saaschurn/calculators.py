def calculate_churn_risk(mrr, mrr_decline_pct, activity_count):
    score = 50
    if mrr_decline_pct > 5:
        score -= 10
    if activity_count < 10:
        score += 10
    return max(0, min(100, score))
