import argparse
import json
import os

from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Use mock data")
    parser.add_argument("--output", choices=["json", "console"], default="console", help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")

    args = parser.parse_args()

    if args.command == "health":
        load_env(args.env)

        stripe = StripeFetcher(stripe_api_key=os.getenv("STRIPE_API_KEY"))
        slack = SlackFetcher(slack_api_token=os.getenv("SLACK_API_TOKEN"))

        if args.dry_run:
            stripe = StripeFetcher(mock=True)
            slack = SlackFetcher(mock=True)

        subscriptions = stripe.fetch_active_subscriptions()
        channel_activity = slack.fetch_channel_activity()

        calculator = ChurnCalculator(subscriptions, channel_activity)
        results = calculator.calculate_churn_risk()

        reporter = Reporter(results)

        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            reporter.print_table()


def load_env(path):
    from dotenv import load_dotenv
    load_dotenv(path)


if __name__ == "__main__":
    main()
