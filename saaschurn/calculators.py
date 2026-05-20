class ChurnCalculator:
    """Calculates churn risk scores based on MRR and activity."""

    def __init__(self):
        self.base_score = 50

    def calculate_risk(self, subscription):
        """Calculate churn risk for a subscription.

        Returns dict with risk score (0-100) and risk level.
        """
        score = self.base_score

        # MRR decline calculation
        current_mrr = subscription.get('current_mrr', 0)
        previous_mrr = subscription.get('previous_mrr', 0)

        if previous_mrr > 0:
            mrr_decline = ((previous_mrr - current_mrr) / previous_mrr) * 100
            if mrr_decline > 5:
                score += 15  # High risk for >5% decline
            elif mrr_decline > 0:
                score += 5   # Low risk for small decline

        # Slack activity calculation
        channel = subscription.get('channel', '')
        activity = subscription.get('activity', {})

        # Calculate daily messages
        if activity:
            total_msgs = activity.get('total_messages', 0)
            days = activity.get('days', 30)
            daily_msgs = total_msgs / days

            if daily_msgs < 10:
                score += 20  # Low activity is high risk
            elif daily_msgs < 25:
                score += 10  # Medium activity

        # Cap score at 100
        score = min(score, 100)

        # Determine risk level
        if score < 30:
            risk_level = 'LOW'
        elif score <= 70:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'

        # Generate recommendation
        recommendation = self._generate_recommendation(score, risk_level)

        return {
            'client': subscription.get('customer_name', 'Unknown'),
            'mrr': current_mrr,
            'activity_score': int(score),
            'churn_risk': risk_level,
            'recommendation': recommendation
        }

    def _generate_recommendation(self, score, risk_level):
        """Generate actionable recommendation based on risk."""
        if risk_level == 'LOW':
            return 'Continue monitoring'
        elif risk_level == 'MEDIUM':
            return 'Schedule check-in call'
        else:
            return 'Immediate outreach required'
