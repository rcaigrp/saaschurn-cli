import argparse
import json
import os
import sys
from dotenv import load_dotenv

from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["json"])
    parser.add_argument("--env", default=".env")

    args = parser.parse_args()

    load_dotenv(args.env)

    stripe_token = os.getenv("STRIPE_API_KEY")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if not stripe_token or not slack_token:
        print("Error: Missing API tokens in env file.")
        sys.exit(1)

    stripe = StripeFetcher(stripe_token)
    slack = SlackFetcher(slack_token)

    if args.dry_run:
        subscriptions = []
        slack_activity = {}
        results = [
            {"client": "ClientA", "mrr": 100.0, "activity_score": 5, "risk_score": 80, "risk_level": "HIGH", "recommendation": "Monitor ClientA (HIGH risk)"},
            {"client": "ClientB", "mrr": 50.0, "activity_score": 20, "risk_score": 50, "risk_level": "MEDIUM", "recommendation": "Monitor ClientB (MEDIUM risk)"},
        ]
    else:
        subscriptions = stripe.fetch_subscriptions()
        # For simplicity, we assume a mapping exists or we just process subscriptions
        # In a real scenario, we'd map client IDs to Slack channels
        slack_activity = {}
        calculator = ChurnCalculator(subscriptions, slack_activity)
        results = []
        # Mock iteration for dry-run style logic
        for sub in subscriptions:
            client_id = sub.get("customer")
            if client_id:
                results.append(calculator.calculate_risk(client_id))

    if args.output == "json":
        print(json.dumps(results))
    else:
        reporter = Reporter()
        reporter.print_table(results)


if __name__ == "__main__":
    main()
