def calculate_mrr(subscriptions):
    mrr = {}
    for sub in subscriptions:
        customer_id = sub.get("customer")
        if customer_id not in mrr:
            mrr[customer_id] = 0
        mrr[customer_id] += sub.get("plan", {}).get("amount", 0) / 100
    return mrr


def calculate_churn_risk(mrr, slack_messages):
    risk_scores = {}
    for client_id, total_mrr in mrr.items():
        score = 50
        if total_mrr < 100:
            score += 20
        msgs = slack_messages.get(client_id, [])
        if len(msgs) < 10:
            score += 20
        risk_scores[client_id] = min(100, score)
    return risk_scores
