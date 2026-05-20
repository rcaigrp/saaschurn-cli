def compute_churn_score(subscriptions, slack_activity):
    scores = []
    for sub in subscriptions:
        mrr = sub.get("mrr", 0)
        score = 0.0
        if mrr < 100:
            score += 0.5
        scores.append({
            "client": sub.get("client"),
            "mrr": mrr,
            "score": score,
            "insight": "Low MRR"
        })
    return scores
