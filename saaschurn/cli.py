import argparse
import json
import os
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls and use mock data")
    parser.add_argument("--output", choices=["json"], help="Export results as JSON")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")

    args = parser.parse_args()

    load_dotenv(dotenv_path=args.env)

    stripe_token = os.environ.get("STRIPE_API_TOKEN")
    slack_token = os.environ.get("SLACK_API_TOKEN")

    if not stripe_token or not slack_token:
        print("Error: STRIPE_API_TOKEN and SLACK_API_TOKEN must be set in environment or .env file")
        sys.exit(1)

    if args.command == "health":
        if args.dry_run:
            print("Running in dry-run mode...")
            mock_data = [
                {"id": "sub_1", "customer_name": "Client A", "mrr": 1000, "mrr_decline": 0},
                {"id": "sub_2", "customer_name": "Client B", "mrr": 500, "mrr_decline": 10},
            ]
            results = ChurnCalculator.calculate_churn(mock_data)
        else:
            stripe_fetcher = StripeFetcher(stripe_token)
            slack_fetcher = SlackFetcher(slack_token)
            subscriptions = stripe_fetcher.fetch_subscriptions()
            channels = slack_fetcher.get_channels()
            activity_data = slack_fetcher.get_channel_activity(channels)
            results = ChurnCalculator.calculate_churn(subscriptions, activity_data)

        reporter = Reporter()
        if args.output == "json":
            print(json.dumps(results, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else o))
        else:
            reporter.print_table(results)

if __name__ == "__main__":
    main()
