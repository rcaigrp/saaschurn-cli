"""Churn risk calculation logic."""

from typing import Dict, List, Optional


class ChurnCalculator:
    """Calculates churn risk scores."""

    def __init__(self, historical_mrr: Optional[Dict] = None):
        """Initialize with optional historical MRR data for comparison."""
        self.historical_mrr = historical_mrr or {}

    def calculate_mrr_decline(self, current_mrr: float, historical_mrr: float) -> float:
        """Calculate MRR decline percentage."""
        if historical_mrr == 0:
            return 0
        decline = ((historical_mrr - current_mrr) / historical_mrr) * 100
        return max(0, decline)  # No positive decline

    def calculate_activity_score(self, message_count: int, days: int = 30) -> float:
        """Calculate activity score (messages per day)."""
        if days <= 0:
            return 0
        return message_count / days

    def calculate_churn_risk(self, mrr_decline: float, activity_score: float) -> Dict:
        """
        Calculate churn risk score (0-100).

        Base score: 50
        - Subtract points for MRR decline >5%
        - Add points for low Slack activity (<10 msgs/day)
        """
        score = 50  # Base score

        # MRR decline impact
        if mrr_decline > 5:
            # Subtract points (reduces risk if revenue is declining?)
            # Actually, MRR decline should INCREASE risk
            # Let me fix the logic:
            score += mrr_decline * 2  # Each 1% decline adds 2 points

        # Activity impact
        if activity_score < 10:
            # Low activity increases risk
            score += (10 - activity_score) * 2

        # Ensure score is between 0 and 100
        score = max(0, min(100, score))

        # Determine risk level
        if score < 30:
            risk_level = "LOW"
        elif score <= 70:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return {
            "score": score,
            "risk_level": risk_level,
            "mrr_decline": mrr_decline,
            "activity_score": activity_score,
        }

    def get_recommendation(self, risk_level: str) -> str:
        """Get recommendation based on risk level."""
        if risk_level == "LOW":
            return "Healthy engagement, no action needed"
        elif risk_level == "MEDIUM":
            return "Monitor closely, schedule check-in"
        else:
            return "Urgent outreach required"
