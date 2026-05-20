import argparse
import sys
import os
import json
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", help="Command to run", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Use mock data")
    parser.add_argument("--output", choices=["json"], default=None, help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")

    args = parser.parse_args()

    if args.command == "health":
        load_dotenv(args.env)
        stripe_token = os.getenv("STRIPE_API_TOKEN", "dummy")
        slack_token = os.getenv("SLACK_API_TOKEN", "dummy")

        if args.dry_run:
            print("Dry-run mode active. Using mock data.")
            results = generate_mock_data()
        else:
            stripe_data = fetch_stripe_data(stripe_token, dry_run=False)
            slack_data = fetch_slack_data(slack_token, dry_run=False)
            results = process_data(stripe_data, slack_data)

        if args.output == "json":
            print(json.dumps(results, default=lambda o: str(o)))
        else:
            generate_report(results)


def generate_mock_data():
    return [
        {
            "client": "Client A",
            "mrr": 1000,
            "activity_score": 80,
            "churn_risk": 50,
            "risk_level": "MEDIUM",
            "recommendation": "Monitor closely"
        }
    ]


def process_data(stripe_data, slack_data):
    results = []
    for sub in stripe_data:
        client = sub.get("client")
        mrr = sub.get("mrr")
        slack_act = next((s for s in slack_data if s["client"] == client), {"score": 0})
        risk = calculate_churn_risk(mrr, slack_act["score"])
        results.append({
            "client": client,
            "mrr": mrr,
            "activity_score": slack_act["score"],
            **risk
        })
    return results