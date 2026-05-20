import argparse
import sys
import os
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import print_table, export_json

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"], help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls and use mock data")
    parser.add_argument("--output", choices=["json"], help="Export results as JSON")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")
    args = parser.parse_args()

    load_dotenv(args.env)
    stripe_token = os.getenv("STRIPE_API_TOKEN")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if args.command == "health":
        if args.dry_run:
            data = [
                {"client": "client-alpha", "mrr": 1000, "activity": 15, "score": 50, "level": "MEDIUM", "recommendation": "Review engagement"},
                {"client": "client-beta", "mrr": 500, "activity": 5, "score": 70, "level": "MEDIUM", "recommendation": "Review engagement"},
                {"client": "client-gamma", "mrr": 200, "activity": 2, "score": 90, "level": "HIGH", "recommendation": "Monitor closely"}
            ]
        else:
            if not stripe_token or not slack_token:
                print("Error: STRIPE_API_TOKEN and SLACK_API_TOKEN must be set.")
                sys.exit(1)
            stripe_subs = fetch_stripe_subscriptions(stripe_token)
            slack_activity = fetch_slack_activity(slack_token)
            data = []
            for sub in stripe_subs:
                client = sub.get("customer_id", "unknown")
                mrr = sub.get("amount", 0) / 100
                previous_mrr = sub.get("previous_amount", 0) / 100
                activity = slack_activity.get(client, 0)
                risk = calculate_churn_risk(mrr, previous_mrr, activity)
                data.append({"client": client, "mrr": mrr, "activity": activity, "score": risk["score"], "level": risk["level"], "recommendation": risk["recommendation"]})

        if args.output == "json":
            export_json(data)
        else:
            print_table(data)

if __name__ == "__main__":
    main()
