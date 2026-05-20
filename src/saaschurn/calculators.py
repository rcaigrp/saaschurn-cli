def calculate_churn_risk(stripe_data, slack_data):
    results = []
    for sub in stripe_data:
        mrr = sub['mrr']
        activity = slack_data.get(sub['id'], 0)
        
        risk = 50
        if mrr < 300: risk += 20
        if activity < 20: risk += 30
        risk = min(risk, 100)
        
        results.append({
            'client': sub['id'],
            'mrr': mrr,
            'activity_score': activity,
            'churn_risk': risk,
            'recommendation': 'HIGH RISK' if risk > 70 else 'MEDIUM RISK' if risk > 30 else 'LOW RISK'
        })
    return results
