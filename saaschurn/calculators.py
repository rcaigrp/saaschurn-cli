def calculate_churn_risk(subscriptions, slack_activity):
    results = []
    for sub in subscriptions:
        customer_id = sub.get('customer_id')
        status = sub.get('status')
        mrr = sub.get('plan', {}).get('amount', 0) / 100
        
        msg_count = slack_activity.get(customer_id, 0)
        activity_score = min(100, max(0, int(msg_count * 2)))
        
        score = 50
        if status != 'active':
            score += 30
        if msg_count < 5:
            score += 30
            
        score = min(100, score)
        risk_level = 'LOW' if score < 30 else ('MEDIUM' if score <= 70 else 'HIGH')
        recommendation = 'Healthy' if score < 30 else ('Monitor' if score <= 70 else 'At Risk')
        
        results.append({
            'client': customer_id,
            'mrr': mrr,
            'activity_score': activity_score,
            'churn_risk': score,
            'risk_level': risk_level,
            'recommendation': recommendation
        })
    return results
