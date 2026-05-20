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
    parser.add_argument("command", type=str, default="health", help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Run with mock data")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal", help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to env file")

    args = parser.parse_args()

    # Load environment variables
    load_dotenv(dotenv_path=args.env)

    # Validate required env vars
    if not args.dry_run:
        if not os.getenv("STRIPE_API_KEY") or not os.getenv("SLACK_APP_TOKEN"):
            print("Error: STRIPE_API_KEY and SLACK_APP_TOKEN must be set in environment or .env file")
            sys.exit(1)

    if args.dry_run:
        print("Running in dry-run mode with mock data...")
        mock_data = [
            {
                "client_id": "client_1",
                "mrr": 1000,
                "activity_score": 15,
                "churn_risk": "HIGH",
                "recommendation": "High Risk: Immediate outreach required"
            },
            {
                "client_id": "client_2",
                "mrr": 5000,
                "activity_score": 80,
                "churn_risk": "LOW",
                "recommendation": "Healthy: Continue monitoring"
            }
        ]
        if args.output == "json":
            print(json.dumps(mock_data))
        else:
            generate_report(mock_data)
        return

    # Fetch real data
    stripe_data = fetch_stripe_data()
    slack_data = fetch_slack_data()

    # Calculate churn risk
    results = calculate_churn_risk(stripe_data, slack_data)

    # Output results
    if args.output == "json":
        print(json.dumps(results))
    else:
        generate_report(results)


if __name__ == "__main__":
    main()
