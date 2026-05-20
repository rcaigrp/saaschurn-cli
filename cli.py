import argparse
import sys
import os
import json
from rich.console import Console
from rich.table import Table
from fetchers import fetch_subscriptions, fetch_slack_activity
from churn import compute_churn_score

console = Console()

def main(args=None):
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("--dry-run", action="store_true", help="Run without real API calls")
    parser.add_argument("--output", type=str, choices=["json"], help="Export findings to JSON")
    
    parsed_args = parser.parse_args(args)

    if not parsed_args.dry_run:
        if not (os.environ.get("STRIPE_API_TOKEN") and os.environ.get("SLACK_API_TOKEN")):
            console.print("[bold red]Missing STRIPE_API_TOKEN or SLACK_API_TOKEN[/bold red]")
            return 1

    subscriptions = fetch_subscriptions(parsed_args.dry_run)
    slack_activity = fetch_slack_activity(parsed_args.dry_run)
    churn_scores = compute_churn_score(subscriptions, slack_activity)

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Client", style="dim")
    table.add_column("MRR", style="green")
    table.add_column("Churn Score", style="red")
    table.add_column("Insight", style="yellow")

    for score in churn_scores:
        table.add_row(score["client"], f"${score['mrr']}", f"{score['score']:.1f}", score["insight"])
    
    console.print(table)

    if parsed_args.output == "json":
        with open("churn_report.json", "w") as f:
            json.dump(churn_scores, f, indent=2)

    return 0

if __name__ == "__main__":
    sys.exit(main())
