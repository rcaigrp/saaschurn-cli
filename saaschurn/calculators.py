class ChurnCalculator:
    def __init__(self, subscriptions, slack_activity):
        self.subscriptions = subscriptions
        self.slack_activity = slack_activity
    
    def calculate_risk_scores(self):
        results = []
        for sub in self.subscriptions:
            client_name = sub.get("customer_name", sub.get("id"))
            mrr = sub.get("mrr", 0)
            channel_name = f"#{client_name.lower().replace(' ', '-')}".replace("(", "").replace(")", "")
            activity = self.slack_activity.get(channel_name, 0)
            
            risk_score = self._calculate_risk(mrr, activity)
            risk_level = self._get_risk_level(risk_score)
            recommendation = self._get_recommendation(risk_level)
            
            results.append({
                "client": client_name,
                "mrr": mrr,
                "activity_score": activity,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": recommendation
            })
        return results
    
    def _calculate_risk(self, mrr, activity):
        score = 50
        # Simplified logic: High MRR but low activity increases risk
        if activity < 10:
            score += 20
        if mrr > 1000:
            score += 10
        return min(100, max(0, score))
    
    def _get_risk_level(self, score):
        if score < 30:
            return "LOW"
        elif score <= 70:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _get_recommendation(self, level):
        if level == "LOW":
            return "No action needed"
        elif level == "MEDIUM":
            return "Schedule check-in"
        else:
            return "Immediate intervention required"
