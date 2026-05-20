def calculate_churn_score(subscriptions, activity):
    # Simple heuristic
    mrr = 0
    for sub in subscriptions.get("data", []):
        mrr += sub.get("amount", 0) * sub.get("quantity", 1)
    
    # Activity drop logic
    recent_msgs = len(activity.get("messages", []))
    
    churn_prob = 0
    if mrr == 0:
        churn_prob = 100
    elif recent_msgs == 0:
        churn_prob = 50
        
    return {
        "MRR": mrr,
        "Recent Messages": recent_msgs,
        "Churn Probability": churn_prob
    }
