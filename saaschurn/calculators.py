def calculate_churn_risk(mrr: float, activity_score: int) -> dict:
    """Calculate churn risk score (0-100) based on MRR and Slack activity."""
    score = 50  # Base score

    # MRR decline logic
    if mrr < 100:
        score += 10

    # Slack activity logic
    if activity_score < 10:
        score += 20
    elif activity_score < 50:
        score += 10

    # Cap at 0-100
    score = max(0, min(100, score))

    if score < 30:
        level = "LOW"
        recommendation = "Healthy engagement."
    elif score <= 70:
        level = "MEDIUM"
        recommendation = "Monitor closely."
    else:
        level = "HIGH"
        recommendation = "At risk of churn."

    return {
        "risk_score": score,
        "risk_level": level,
        "recommendation": recommendation
    }
