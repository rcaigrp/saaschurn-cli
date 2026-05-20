def calculate_churn_risk(mrr, mrr_decline_rate=0, slack_messages=0):
    score = 50
    
    if mrr_decline_rate > 5:
        score -= 10
        
    if slack_messages < 10:
        score += 10
        
    score = max(0, min(100, score))
    
    if score < 30:
        risk_level = "LOW"
    elif score <= 70:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"
        
    return score, risk_level
