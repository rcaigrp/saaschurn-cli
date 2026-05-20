def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions.get('data', []):
        mrr += sub.get('plan', {}).get('amount', 0)
    return mrr

def calculate_churn_score(mrr_data, slack_activity_data):
    score = 50
    if mrr_data.get('decline', 0) > 5:
        score -= 10
    if slack_activity_data.get('activity', 0) < 10:
        score += 20
    return score
