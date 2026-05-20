#!/usr/bin/env python3
"""MRR and churn risk calculation logic"""


class ChurnCalculator:
    """Calculates churn risk scores based on MRR decline and Slack activity."""

    def __init__(self):
        self.base_score = 50

    def calculate_risk(self, mrr_decline=0, slack_activity_drop=0):
        """
        Calculate churn risk score (0-100).

        Args:
            mrr_decline: Percentage decline in MRR
            slack_activity_drop: Percentage drop in Slack activity

        Returns:
            dict with risk_score, risk_level, and recommendation
        """
        score = self.base_score

        # Subtract points for MRR decline > 5%
        if mrr_decline > 5:
            score -= (mrr_decline - 5) * 2

        # Add points for low Slack activity (< 10 msgs/day)
        if slack_activity_drop > 50:
            score += slack_activity_drop * 0.3

        # Clamp score to 0-100
        score = max(0, min(100, score))

        # Determine risk level
        if score < 30:
            risk_level = 'LOW'
            recommendation = 'Monitor - healthy engagement'
        elif score <= 70:
            risk_level = 'MEDIUM'
            recommendation = 'Engage - schedule check-in'
        else:
            risk_level = 'HIGH'
            recommendation = 'Escalate - immediate outreach needed'

        return {
            'risk_score': round(score, 1),
            'risk_level': risk_level,
            'recommendation': recommendation
        }
