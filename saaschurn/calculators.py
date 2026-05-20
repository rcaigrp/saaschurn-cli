import os


class ChurnCalculator:
    def __init__(self):
        self.mrr_threshold = 100000  # MRR in cents
        self.activity_threshold = 10  # Messages per day

    def calculate(self, stripe_data, slack_data):
        results = []

        for sub in stripe_data:
            if sub.get('status') != 'active':
                continue

            customer_name = sub.get('customer_name', 'Unknown')
            current_mrr = sub.get('current_period_amount', 0) / 100  # Convert cents to dollars
            previous_mrr = sub.get('previous_period_amount', current_mrr) / 100

            # Calculate MRR decline percentage
            if previous_mrr > 0:
                mrr_decline = ((previous_mrr - current_mrr) / previous_mrr) * 100
            else:
                mrr_decline = 0

            # Get Slack activity
            activity = slack_data.get(customer_name, {})
            message_count = activity.get('message_count', 0)

            # Calculate churn risk score
            score = 50  # Base score

            # Subtract points for MRR decline > 5%
            if mrr_decline > 5:
                score -= 10

            # Add points for low Slack activity (<10 msgs/day)
            if message_count < 10:
                score += 10

            # Clamp score between 0 and 100
            score = max(0, min(100, score))

            # Determine risk level
            if score < 30:
                risk_level = 'LOW'
                recommendation = 'Continue monitoring'
            elif score <= 70:
                risk_level = 'MEDIUM'
                recommendation = 'Schedule check-in meeting'
            else:
                risk_level = 'HIGH'
                recommendation = 'Immediate outreach required'

            results.append({
                'client': customer_name,
                'mrr': current_mrr,
                'activity_score': message_count,
                'churn_risk': score,
                'risk_level': risk_level,
                'recommendation': recommendation
            })

        return results
