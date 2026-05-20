class ChurnRisk:
    def __init__(self, client_name, mrr, activity_score, risk_score, recommendation):
        self.client_name = client_name
        self.mrr = mrr
        self.activity_score = activity_score
        self.risk_score = risk_score
        self.recommendation = recommendation

class ChurnCalculator:
    @staticmethod
    def calculate_churn(subscriptions, slack_activity=None):
        results = []
        for sub in subscriptions:
            client_name = sub.get("customer_name", "Unknown")
            mrr = sub.get("mrr", 0)
            mrr_decline = sub.get("mrr_decline", 0)
            slack_activity_score = slack_activity.get(client_name, 0) if slack_activity else 0
            
            risk_score = 50
            if mrr_decline > 5:
                risk_score -= 10
            if slack_activity_score < 10:
                risk_score += 20
                
            risk_level = "LOW" if risk_score < 30 else "MEDIUM" if risk_score <= 70 else "HIGH"
            recommendation = "Monitor" if risk_level == "MEDIUM" else "Action Needed" if risk_level == "HIGH" else "Healthy"
            
            results.append(ChurnRisk(client_name, mrr, slack_activity_score, risk_score, recommendation))
        return results
