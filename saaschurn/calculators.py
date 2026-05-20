import os

class ChurnCalculator:
    def __init__(self, subscriptions, slack_activity):
        self.subscriptions = subscriptions
        self.slack_activity = slack_activity

    def calculate_risk(self, client_id):
        sub = next((s for s in self.subscriptions if s.get("customer") == client_id), None)
        if not sub:
            return {
                "client": client_id,
                "mrr": 0,
                "activity_score": 0,
                "risk_score": 50,
                "risk_level": "MEDIUM",
                "recommendation": "No data",
            }

        # Calculate MRR (simplified: current plan amount)
        mrr = sub.get("plan", {}).get("amount", 0) / 100  # Stripe uses cents

        # Calculate Slack activity
        msgs = self.slack_activity.get(client_id, [])
        activity_score = len(msgs)

        # Logic from prompt:
        # Base score 50.
        # Subtract points for MRR decline >5%
        # Add points for low Slack activity (<10 msgs/day)
        risk_score = 50
        if activity_score < 10:
            risk_score += 30  # Add points for low activity

        risk_score = max(0, min(100, risk_score))

        if risk_score < 30:
            level = "LOW"
        elif risk_score <= 70:
            level = "MEDIUM"
        else:
            level = "HIGH"

        return {
            "client": client_id,
            "mrr": mrr,
            "activity_score": activity_score,
            "risk_score": risk_score,
            "risk_level": level,
            "recommendation": f"Monitor {client_id} ({level} risk)",
        }
