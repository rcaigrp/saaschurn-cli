def calculate_churn_risk(subscriptions, slack_activity):
    results = []
    for cid, mrr in subscriptions.items():
        score = 50
        activity = slack_activity.get(cid, 0)
        
        if activity < 10:
            score += 30  # High penalty for low activity
            
        if score < 30:
            risk = 'LOW'
        elif score <= 70:
            risk = 'MEDIUM'
        else:
            risk = 'HIGH'
            
        rec = 'No action needed' if risk == 'LOW' else 'Monitor closely' if risk == 'MEDIUM' else 'High churn risk'
        results.append({'client_id': cid, 'mrr': mrr, 'activity_score': activity, 'churn_risk': risk, 'recommendation': rec})
    return results