def calculate_mrr(subscriptions):
    mrr = {}
    for sub in subscriptions:
        customer_name = sub.get("customer_name", sub.get("customer", "Unknown"))
        price = sub.get("price", 0)
        quantity = sub.get("quantity", 1)
        mrr[customer_name] = price * quantity
    return mrr

def calculate_churn_risk(mrr, slack_activity):
    results = []
    for client, score_mrr in mrr.items():
        base_score = 50
        activity = slack_activity.get(client, {}).get("messages_count", 0)
        if activity < 10:
            base_score += 20
        elif activity < 50:
            base_score += 10
            
        risk_level = "LOW"
        if base_score > 70:
            risk_level = "HIGH"
        elif base_score > 30:
            risk_level = "MEDIUM"
            
        results.append({
            "client": client,
            "mrr": score_mrr,
            "activity_score": activity,
            "churn_risk": base_score,
            "risk_level": risk_level,
            "recommendation": "Monitor closely" if risk_level == "HIGH" else "Good health"
        })
    return results
