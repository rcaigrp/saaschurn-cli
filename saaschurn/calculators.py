class ChurnCalculator:
    def __init__(self, subscriptions, channel_activity):
        self.subscriptions = subscriptions
        self.channel_activity = channel_activity

    def calculate_churn_risk(self):
        results = []
        for sub in self.subscriptions:
            customer_id = sub.get("customer_id")
            mrr = sub.get("amount", 0) / 100  # Stripe returns amount in cents
            # Find activity
            activity = next((a for a in self.channel_activity if a["customer_id"] == customer_id), None)
            activity_score = 100 if activity else 0
            if activity:
                # Mock logic: if message_count < 10, score is low
                if activity["message_count"] < 10:
                    activity_score = 10
                else:
                    activity_score = 100

            # Risk score
            risk_score = 50
            if mrr < 100:  # Low MRR
                risk_score += 20
            if activity_score < 50:
                risk_score += 30

            risk_level = "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 30 else "LOW"
            results.append({
                "customer_id": customer_id,
                "mrr": mrr,
                "activity_score": activity_score,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": self._get_recommendation(risk_level)
            })
        return results

    def _get_recommendation(self, risk_level):
        if risk_level == "HIGH":
            return "Immediate outreach required"
        elif risk_level == "MEDIUM":
            return "Schedule check-in"
        else:
            return "No action needed"
