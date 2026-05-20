import argparse
import json
import sys
from rich.console import Console
from rich.table import Table
from saaschurn.stripe_client import fetch_active_subscriptions, calculate_mrr
from saaschurn.slack_client import fetch_channel_activity
from saaschurn.churn_calculator import compute_churn_score

console = Console()

def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', choices=['json', 'rich'], default='rich')
    args = parser.parse_args()

    stripe_token = "fake_stripe_token"
    slack_token = "fake_slack_token"

    if args.dry_run:
        console.print("[bold green]Dry run mode enabled.[/bold green]")
        return

    subs = fetch_active_subscriptions(stripe_token)
    mrr = calculate_mrr(subs)
    activity = fetch_channel_activity(slack_token, ["C123"])
    
    score = compute_churn_score(mrr, activity)
    
    if args.output == 'json':
        print(json.dumps({'mrr': mrr, 'churn_score': score}))
    else:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="dim_cyan")
        table.add_row("MRR", f"${mrr:.2f}")
        table.add_row("Churn Score", f"{score:.2f}")
        console.print(table)

if __name__ == '__main__':
    main()
