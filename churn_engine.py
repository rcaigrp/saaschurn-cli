import stripe
import slack_sdk

def fetch_subscriptions(token):
    stripe.api_key = token
    return stripe.Subscription.list(status="active").data

def fetch_slack_activity(token):
    client = slack_sdk.WebClient(token=token)
    return 10

def compute_churn_score(mrr, slack_activity):
    score = 0
    if mrr < 100: score += 0.5
    if slack_activity < 5: score += 0.5
    return score
