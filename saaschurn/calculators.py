def calculate_mrr(subscriptions):
    mrr = {}
    for sub in subscriptions:
        if sub.get("status") != "active":
            continue
        name = sub.get("customer_name", "Unknown")
        price = sub.get("plan", {}).get("amount", 0)
        qty = sub.get("quantity", 1)
        mrr_val = (price * qty) / 100
        mrr[name] = mrr_val
    return mrr

def calculate_churn_risk(mrr_data, slack_data):
    risk = {}
    for client, mrr in mrr_data.items():
        score = 50
        activity = slack_data.get(client, 0)
        if activity < 10:
            score += 20
        risk[client] = {
            "mrr": mrr,
            "activity": activity,
            "score": score,
            "level": "LOW" if score < 30 else "MEDIUM" if score <= 70 else "HIGH",
            "recommendation": "Monitor" if score < 50 else "Investigate"
        }
    return risk
