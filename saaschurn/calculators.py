"""Churn risk calculation logic."""

class ChurnCalculator:
    def calculate_risk(self, subscriptions, slack_activity):
        results = []
        for sub in subscriptions:
            customer_id = sub.get('customer')
            mrr = sub.get('plan', {}).get('unit_amount', 0) / 1000  # Convert cents to dollars
            
            # Find slack activity
            activity = next((a for a in slack_activity if a.get('channel') == customer_id), None)
            msg_count = activity.get('messages', 0) if activity else 0
            
            # Calculate risk score (0-100)
            risk_score = 50  # Base score
            if mrr < 100:  # Low MRR
                risk_score += 20
            if msg_count < 10:  # Low activity
                risk_score += 30
            
            risk_level = "LOW" if risk_score < 30 else "MEDIUM" if risk_score <= 70 else "HIGH"
            
            results.append({
                "client": customer_id,
                "mrr": mrr,
                "activity_score": msg_count,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": self._get_recommendation(risk_level)
            })
        return results

    def _get_recommendation(self, level):
        if level == "LOW":
            return "No action needed"
        elif level == "MEDIUM":
            return "Monitor closely"
        else:
            return "Immediate outreach required"
