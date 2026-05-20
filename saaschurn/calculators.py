from typing import List, Dict


def calculate_churn_report(stripe_data: List[dict], slack_data: Dict[str, dict]) -> List[dict]:
    """Calculate churn risk scores based on MRR decline and Slack activity.
    
    Args:
        stripe_data: List of subscription data from Stripe.
        slack_data: Dict of Slack activity data.
        
    Returns:
        List of churn report data with risk scores and recommendations.
    """
    report = []
    
    # Thresholds
    MRR_DECLINE_THRESHOLD = 5  # Percentage
    LOW_ACTIVITY_THRESHOLD = 10  # Messages per day
    
    for client_data in stripe_data:
        client_name = client_data.get("client", "Unknown")
        mrr = client_data.get("mrr", 0.0)
        previous_mrr = client_data.get("previous_mrr", 0.0)
        
        # Calculate MRR decline
        if previous_mrr > 0:
            mrr_decline_pct = ((previous_mrr - mrr) / previous_mrr) * 100
        else:
            mrr_decline_pct = 0
        
        # Get Slack activity
        slack_info = slack_data.get(client_name, {})
        avg_msgs = slack_info.get("avg_msgs_per_day", 0)
        
        # Calculate risk score (0-100)
        risk_score = 50  # Base score
        
        # Subtract points for MRR decline >5%
        if mrr_decline_pct > MRR_DECLINE_THRESHOLD:
            risk_score -= 10
        
        # Add points for low Slack activity (<10 msgs/day)
        if avg_msgs < LOW_ACTIVITY_THRESHOLD:
            risk_score += 15
        
        # Clamp score between 0 and 100
        risk_score = max(0, min(100, risk_score))
        
        # Determine risk level
        if risk_score < 30:
            risk_level = "LOW"
            recommendation = "Maintain engagement"
        elif risk_score <= 70:
            risk_level = "MEDIUM"
            recommendation = "Schedule check-in meeting"
        else:
            risk_level = "HIGH"
            recommendation = "Immediate intervention required"
        
        report.append({
            "client": client_name,
            "mrr": round(mrr, 2),
            "activity_score": round(avg_msgs, 1),
            "churn_risk": risk_score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "mrr_decline_pct": round(mrr_decline_pct, 1),
            "stripe_id": client_data.get("stripe_id", "")
        })
    
    return report
