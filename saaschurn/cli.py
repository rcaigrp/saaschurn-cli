import argparse
import json
import os
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import print_report


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, use mock data")
    parser.add_argument("--output", choices=["json"], help="Export results as JSON")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    args = parser.parse_args()

    if args.command == "health":
        run_health(args)


def run_health(args):
    load_dotenv(args.env)
    stripe_token = os.environ.get("STRIPE_API_TOKEN")
    slack_token = os.environ.get("SLACK_API_TOKEN")
    if not stripe_token or not slack_token:
        print("Error: STRIPE_API_TOKEN and SLACK_API_TOKEN must be set.")
        return

    if args.dry_run:
        data = get_mock_data()
    else:
        stripe_subs = fetch_stripe_subscriptions(stripe_token)
        # Extract channels from metadata
        client_channels = {}
        for sub in stripe_subs:
            cid = sub.get("customer_id")
            channel = sub.get("metadata", {}).get("slack_channel")
            if channel and cid:
                client_channels[cid] = channel
        slack_activity = fetch_slack_activity(slack_token, client_channels)
        data = process_data(stripe_subs, slack_activity)

    if args.output == "json":
        print(json.dumps(data, indent=2))
    else:
        print_report(data)


def get_mock_data():
    return [
        {"client": "Acme Corp", "mrr": 1000, "activity_score": 50, "churn_risk": 65, "recommendation": "MEDIUM"},
        {"client": "Globex Inc", "mrr": 2000, "activity_score": 80, "churn_risk": 30, "recommendation": "LOW"}
    ]


def process_data(stripe_subs, slack_activity):
    data = []
    for sub in stripe_subs:
        client_id = sub.get("customer_id")
        mrr = sub.get("current_period_amount", 0) / 100
        # Find channel for this client
        channel = sub.get("metadata", {}).get("slack_channel")
        activity_count = 0
        if channel and channel in slack_activity:
            activity_count = slack_activity[channel]

        # Calculate risk
        risk_score = calculate_churn_risk(mrr, 0, activity_count)

        recommendation = "LOW" if risk_score < 30 else ("MEDIUM" if risk_score < 70 else "HIGH")

        data.append({
            "client": sub.get("customer_name", client_id),
            "mrr": mrr,
            "activity_score": activity_count,
            "churn_risk": risk_score,
            "recommendation": recommendation
        })
    return data
