import argparse
import json
import sys
import os
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_table

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls and use mock data")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal", help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")
    
    args = parser.parse_args()
    load_dotenv(args.env)
    
    if args.dry_run:
        print("Running in dry-run mode...")
        subscriptions = [
            {"id": "sub_1", "customer_name": "Client A", "status": "active", "recurring_intervals": {"amount": 1000, "currency": "usd"}},
            {"id": "sub_2", "customer_name": "Client B", "status": "active", "recurring_intervals": {"amount": 500, "currency": "usd"}}
        ]
        slack_activity = {"Client A": 100, "Client B": 10}
    else:
        stripe_token = os.getenv("STRIPE_API_KEY")
        slack_token = os.getenv("SLACK_API_TOKEN")
        if not stripe_token or not slack_token:
            print("Error: Missing API tokens. Set STRIPE_API_KEY and SLACK_API_TOKEN.")
            sys.exit(1)
        subscriptions = fetch_stripe_subscriptions(stripe_token)
        slack_activity = fetch_slack_activity(slack_token)
    
    results = []
    for sub in subscriptions:
        risk = calculate_churn_risk(sub, slack_activity.get(sub.get("customer_name"), 0))
        results.append({
            "Client": sub.get("customer_name"),
            "MRR": sub.get("recurring_intervals", {}).get("amount", 0) / 100,
            "Activity Score": slack_activity.get(sub.get("customer_name"), 0),
            "Churn Risk": risk["score"],
            "Recommendation": risk["level"]
        })
    
    if args.output == "json":
        print(json.dumps(results))
    else:
        generate_table(results)

if __name__ == "__main__":
    main()
