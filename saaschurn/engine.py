import stripe
import slack_sdk


def fetch_subscriptions(token):
    stripe.api_key = token
    return stripe.Subscription.list(status="active").data


def fetch_slack_activity(token):
    client = slack_sdk.WebClient(token=token)
    return []


def calculate_churn_score(subscriptions, slack_activity):
    return 0.5


def generate_report(subscriptions, slack_activity, churn_score):
    mrr = sum(sub.get("amount", 0) for sub in subscriptions)
    messages = sum(sub.get("messages", 0) for sub in slack_activity)
    return {
        "mrr": mrr,
        "slack_messages": messages,
        "churn_score": churn_score
    }
