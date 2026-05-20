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
    parser.add_argument("command", help="health")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal")
    parser.add_argument("--env", default=".env")
    args = parser.parse_args()

    load_dotenv(args.env)

    stripe_key = os.getenv("STRIPE_API_KEY")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if args.dry_run:
        data = [
            {
                "client": "Mock Client",
                "mrr": 1000.0,
                "activity": 5,
                "risk": 70,
                "recommendation": "Monitor closely",
            }
        ]
    else:
        if not stripe_key or not slack_token:
            print("Error: STRIPE_API_KEY and SLACK_API_TOKEN must be set.", file=sys.stderr)
            sys.exit(1)

        stripe = StripeFetcher(stripe_key)
        slack = SlackFetcher(slack_token)
        subs = stripe.fetch_subscriptions()
        calc = ChurnCalculator()
        data = []
        for sub in subs:
            mrr = sub.get("plan", {}).get("amount", 0) / 100
            channel = sub.get("metadata", {}).get("slack_channel")
            slack_msgs = 0
            if channel:
                slack_msgs = slack.fetch_channel_activity(channel)
            risk = calc.calculate_risk(mrr, mrr, slack_msgs)
            data.append(
                {
                    "client": sub.get("customer_id"),
                    "mrr": mrr,
                    "activity": slack_msgs,
                    "risk": risk,
                    "recommendation": "Check Slack activity" if slack_msgs < 10 else "Healthy",
                }
            )

    if args.output == "json":
        print(json.dumps(data))
    else:
        Reporter().print_table(data)


if __name__ == "__main__":
    main()