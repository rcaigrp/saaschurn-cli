import os
import argparse
import json
import stripe
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def fetch_subscriptions(stripe_token):
    stripe.api_key = stripe_token
    try:
        data = stripe.Subscription.list(limit=50)
        return [s for s in data.data if s.status == 'active']
    except Exception as e:
        console.print(f'[bold red]Stripe Error: {e}[/bold red]')
        return []

def calculate_mrr(subscriptions):
    mrr = 0
    for sub in subscriptions:
        if hasattr(sub, 'plan') and hasattr(sub.plan, 'amount'):
            mrr += sub.plan.amount / 100
    return mrr

def fetch_slack_activity(slack_token, channels):
    headers = {'Authorization': f'Bearer {slack_token}'}
    for ch in channels:
        resp = requests.get('https://slack.com/api/conversations.history', headers=headers, params={'channel': ch})
        if resp.status_code == 200:
            pass
    return channels

def compute_churn_score(mrr, activity_count):
    if mrr < 1000 or activity_count == 0:
        return 0.8
    return 0.2

def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', choices=['console', 'json'], default='console')
    args = parser.parse_args()

    stripe_token = os.environ.get('STRIPE_API_TOKEN')
    slack_token = os.environ.get('SLACK_API_TOKEN')

    if not stripe_token or not slack_token:
        console.print('[bold red]Missing env vars: STRIPE_API_TOKEN or SLACK_API_TOKEN![/bold red]')
        return

    if args.dry_run:
        console.print('[bold yellow]Dry-run mode enabled. No real data fetched.[/bold yellow]')
        return

    subs = fetch_subscriptions(stripe_token)
    mrr = calculate_mrr(subs)
    
    channels = ['client-channel-1'] 
    fetch_slack_activity(slack_token, channels)
    
    score = compute_churn_score(mrr, 0)

    if args.output == 'json':
        result = {
            'mrr': mrr,
            'churn_score': score,
            'active_subscriptions': len(subs)
        }
        console.print(json.dumps(result))
    else:
        table = Table()
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("MRR", f"${mrr:.2f}")
        table.add_row("Churn Score", f"{score:.2f}")
        table.add_row("Active Subs", str(len(subs)))
        console.print(table)

if __name__ == '__main__':
    main()
