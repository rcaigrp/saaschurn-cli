import argparse
import json
import os
import sys
from rich.console import Console
from churn import get_subscriptions, calculate_mrr, get_slack_activity, compute_churn_score

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument('--dry-run', action='store_true', help='Run without actual API calls')
    parser.add_argument('--output', choices=['console', 'json'], default='console', help='Output format')
    parser.add_argument('channels', nargs='*', help='Slack channels to check')
    
    args = parser.parse_args()
    
    # 1. Authenticate via env vars
    stripe_token = os.getenv('STRIPE_API_TOKEN')
    slack_token = os.getenv('SLACK_API_TOKEN')
    
    if not stripe_token or not slack_token:
        Console().print("[bold red]Error: Missing STRIPE_API_TOKEN or SLACK_API_TOKEN[/bold red]")
        sys.exit(1)
        
    # 2. Fetch active subscriptions
    subscriptions = get_subscriptions(stripe_token, dry_run=args.dry_run)
    mrr = calculate_mrr(subscriptions)
    
    # 3. Pull Slack activity
    channels = args.channels or ['general']
    activity = get_slack_activity(slack_token, channels, dry_run=args.dry_run)
    
    # 4. Compute churn score
    score = compute_churn_score(mrr, activity)
    
    # 5 & 6. Output
    result = {'mrr': mrr, 'activity': activity, 'churn_score': score}
    
    if args.output == 'json':
        print(json.dumps(result))
    else:
        console = Console()
        console.print(f"[bold]MRR: ${mrr}[/bold]")
        console.print(f"[bold]Churn Score: {score:.2f}[/bold]")

if __name__ == '__main__':
    main()
