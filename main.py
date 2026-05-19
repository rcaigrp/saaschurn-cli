import os
import requests
import json
from rich.console import Console

console = Console()

def get_env_vars():
    stripe_key = os.getenv('STRIPE_API_KEY')
    slack_token = os.getenv('SLACK_API_TOKEN')
    if not stripe_key or not slack_token:
        raise ValueError("Missing Stripe or Slack API tokens in environment variables.")
    return stripe_key, slack_token

def fetch_subscriptions(stripe_key):
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {stripe_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions.get('data', []):
        if sub.get('status') == 'active':
            mrr += sub.get('plan', {}).get('amount', 0) / 100
    return mrr

def fetch_slack_activity(slack_token, channel):
    url = f"https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {slack_token}", "Content-Type": "application/json"}
    params = {"channel": channel}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def calculate_churn_score(mrr_history, slack_activity_history):
    revenue_decline = 1 - (mrr_history[-1] / mrr_history[0] if mrr_history[0] > 0 else 1)
    activity_drop = 1 - (slack_activity_history[-1] / slack_activity_history[0] if slack_activity_history[0] > 0 else 1)
    return revenue_decline * 0.6 + activity_drop * 0.4

def generate_report(data):
    console.print(f"[bold red]Churn Risk Report[/bold red]")
    console.print(f"MRR: ${data['mrr']}")
    console.print(f"Churn Score: {data['churn_score']}")

def main():
    stripe_key, slack_token = get_env_vars()
    subscriptions = fetch_subscriptions(stripe_key)
    mrr = calculate_mrr(subscriptions)
    slack_logs = fetch_slack_activity(slack_token, 'general')
    churn_score = calculate_churn_score([1000, 800], [10, 5])
    generate_report({'mrr': mrr, 'churn_score': churn_score})

if __name__ == "__main__":
    main()
