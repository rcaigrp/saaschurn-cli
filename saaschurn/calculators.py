def calculate_churn_risk(stripe_data, slack_data):
    """Calculate churn risk score (0-100) for each client.
    
    Base score starts at 50.
    - Subtract points for MRR decline >5%
    - Subtract points for low Slack activity (<10 msgs/day)
    - Return risk level: LOW (<30), MEDIUM (30-70), HIGH (>70)
    """
    results = {}
    
    # Map customer IDs to slack channels (assume same name)
    customer_slack_map = {}
    for sub_id in stripe_data:
        # Try to find matching slack channel
        for channel_name in slack_data:
            if sub_id.lower() in channel_name.lower() or channel_name.lower() in sub_id.lower():
                customer_slack_map[sub_id] = channel_name
                break
    
    for customer_id, sub_info in stripe_data.items():
        base_score = 50
        risk_score = base_score
        
        # Check MRR decline
        if sub_info.get("has_declined"):
            risk_score -= 20  # Significant decline
        
        # Check Slack activity
        channel_name = customer_slack_map.get(customer_id)
        if channel_name and channel_name in slack_data:
            activity = slack_data[channel_name]
            avg_daily = activity.get("avg_daily", 0)
            
            # Low activity increases risk
            if avg_daily < 1:
                risk_score -= 25  # Very low activity
            elif avg_daily < 5:
                risk_score -= 15  # Low activity
            elif avg_daily >= 10:
                risk_score -= 5  # Good activity
        else:
            # No slack data - unknown risk
            risk_score -= 10
        
        # Clamp score to 0-100
        risk_score = max(0, min(100, risk_score))
        
        # Determine risk level
        if risk_score < 30:
            risk_level = "LOW"
            recommendation = "Healthy: Continue monitoring"
        elif risk_score <= 70:
            risk_level = "MEDIUM"
            recommendation = "At risk: Schedule check-in call"
        else:
            risk_level = "HIGH"
            recommendation = "High Risk: Immediate outreach required"
        
        # Calculate activity score (0-100)
        if channel_name and channel_name in slack_data:
            activity = slack_data[channel_name]
            avg_daily = activity.get("avg_daily", 0)
            activity_score = min(100, max(0, int(avg_daily * 10)))
        else:
            activity_score = 0
        
        results[customer_id] = {
            "client_id": customer_id,
            "mrr": sub_info["mrr"],
            "activity_score": activity_score,
            "churn_risk": risk_level,
            "risk_score": risk_score,
            "recommendation": recommendation
        }
    
    return results
