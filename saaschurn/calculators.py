def calculate_churn_risk(stripe_data, slack_data):
    results = []
    for sub in stripe_data:
        mrr = sub.get("mrr", 0)
        activity = 0
        for ch in slack_data:
            if ch.get("customer_id") == sub.get("customer_id"):
                activity = ch.get("messages", 0)

        risk_score = 50 - (mrr * 0.1) + (activity * 0.5)
        risk_score = max(0, min(100, risk_score))

        risk_level = "LOW" if risk_score < 30 else ("MEDIUM" if risk_score < 70 else "HIGH")

        results.append({
            "customer_id": sub.get("customer_id"),
            "mrr": mrr,
            "activity_score": activity,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": f"Monitor {risk_level} risk"
        })
    return results
