"""CLI interface for SaaS Churn tool."""
import argparse
import json
import os

from dotenv import load_dotenv
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn Prediction CLI Tool")
    parser.add_argument("command", choices=["health"], help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Use mock data instead of API calls")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal", help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")
    args = parser.parse_args()

    # Load environment variables
    load_dotenv(args.env)

    # Validate required environment variables
    stripe_token = os.getenv("STRIPE_API_TOKEN")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if not stripe_token or not slack_token:
        print("Error: STRIPE_API_TOKEN and SLACK_API_TOKEN must be set in .env file")
        return

    # Fetch data
    stripe_fetcher = StripeFetcher(stripe_token)
    slack_fetcher = SlackFetcher(slack_token)

    if args.dry_run:
        # Use mock data
        subscriptions = [
            {"customer_name": "Acme Corp", "mrr": 1000, "previous_mrr": 1100, "id": "sub_1"},
            {"customer_name": "Globex Inc", "mrr": 2000, "previous_mrr": 2000, "id": "sub_2"},
            {"customer_name": "Initech", "mrr": 500, "previous_mrr": 600, "id": "sub_3"},
        ]
            channels = [
            {"customer_name": "Acme Corp", "channel_name": "#acme-support", "message_count": 5},
            {"customer_name": "Globex Inc", "channel_name": "#globex-team", "message_count": 150},
            {"customer_name": "Initech", "channel_name": "#initech-support", "message_count": 2},
        ]
    else:
        # Fetch real data
        subscriptions = stripe_fetcher.get_active_subscriptions()
        channels = slack_fetcher.get_channel_activity()

    # Calculate churn risk
    calculator = ChurnCalculator(subscriptions, channels)
    results = calculator.calculate_risk_scores()

    # Generate report
    reporter = Reporter()

    if args.output == "json":
        # Output as JSON
        print(json.dumps(results, indent=2))
    else:
        # Output as terminal table
        reporter.print_report(results)


if __name__ == "__main__":
    main()
