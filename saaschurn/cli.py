import argparse
import os
import json
import sys
from rich.table import Table
from rich.console import Console

from saaschurn.stripe_client import get_active_subscriptions, calc_mrr
from saaschurn.slack_client import get_channel_activity
from saaschurn.churn_calculator import calculate_churn_score

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without API calls")
    parser.add_argument("--output", choices=["json", "rich"], default="rich", help="Output format")
    args = parser.parse_args()

    console = Console()
    stripe_token = os.getenv("STRIPE_API_TOKEN")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if not stripe_token or not slack_token:
        console.print("[bold red]Missing env vars STRIPE_API_TOKEN or SLACK_API_TOKEN[/bold red]")
        sys.exit(1)

    if args.dry_run:
        console.print("[bold green]Dry-run mode active. Simulating data.[/bold green]")
        subscriptions = [{"plan": {"amount": 1000}}]
        activity = {"message_count": 10, "last_message": "hello"}
        mrr = calc_mrr(subscriptions)
    else:
        subscriptions = get_active_subscriptions(stripe_token)
        activity = get_channel_activity(slack_token, ["#churn-alerts"])
        mrr = calc_mrr(subscriptions)

    score = calculate_churn_score(mrr, activity)

    if args.output == "json":
        data = {
            "mrr": mrr,
            "activity": activity,
            "churn_score": score
        }
        print(json.dumps(data, indent=2))
    else:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Metric", style="dim", width=15)
        table.add_column("Value", style="bright_green")
        table.add_row("MRR", f"${mrr:.2f}")
        table.add_row("Activity", f"{activity.get('message_count', 0)} msgs")
        table.add_row("Churn Score", f"{score}")
        console.print(table)

if __name__ == "__main__":
    main()
