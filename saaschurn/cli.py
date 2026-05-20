import argparse
import os
import json
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_mrr, calculate_churn_risk, get_risk_level
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["json"])
    parser.add_argument("--env", type=str, default=".env")

    args = parser.parse_args()

    load_dotenv(args.env)
    stripe_token = os.getenv("STRIPE_API_TOKEN")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if not stripe_token or not slack_token:
        print("Error: Missing Stripe or Slack API tokens in environment variables.")
        return

    if args.dry_run:
        results = [
            {"client": "Acme Corp", "mrr": 5000.0, "activity": 5, "risk_score": 75, "risk_level": "HIGH", "recommendation": "Immediate outreach required."},
            {"client": "Globex Inc", "mrr": 1500.0, "activity": 45, "risk_score": 35, "risk_level": "MEDIUM", "recommendation": "Monitor closely."}
        ]
    else:
        subs = fetch_stripe_subscriptions(stripe_token)
        channel_ids = [sub.get("customer_id") for sub in subs]
        activity = fetch_slack_activity(slack_token, channel_ids)
        
        results = []
        for sub in subs:
            client = sub.get("customer_id")
            mrr = calculate_mrr(sub)
            act_score = activity.get(client, 0)
            risk_score = calculate_churn_risk(mrr, act_score)
            risk_level = get_risk_level(risk_score)
            results.append({
                "client": client,
                "mrr": mrr,
                "activity": act_score,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": f"Focus on {risk_level} risk."
            })

    if args.output == "json":
        print(json.dumps(results, default=str))
    else:
        generate_report(results)

if __name__ == "__main__":
    main()