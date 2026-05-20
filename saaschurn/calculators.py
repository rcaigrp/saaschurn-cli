def calculate_churn_risk(mrr, activity_score):
    score = 50
    if mrr < 500:
        score += 20
    if activity_score < 10:
        score += 30
        
    score = max(0, min(100, score))
    
    if score < 30:
        level = "LOW"
        rec = "Engage proactively"
    elif score <= 70:
        level = "MEDIUM"
        rec = "Monitor closely"
    else:
        level = "HIGH"
        rec = "Immediate outreach required"
        
    return {
        "churn_risk": score,
        "risk_level": level,
        "recommendation": rec
    }