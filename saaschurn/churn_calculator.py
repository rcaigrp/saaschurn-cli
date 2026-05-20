def calculate_churn_score(mrr, activity):
    score = 0
    if mrr < 100:
        score += 50
    if activity.get("message_count", 0) < 5:
        score += 30
    if activity.get("last_message", "") == "":
        score += 20
    return score
