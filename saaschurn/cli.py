import argparse
import json
import os
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report


def main():
    parser = argparse.ArgumentParser(description="SaaSChurn CLI Tool")
    parser.add_argument("command", help="Command to run (e.g., health)")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, use mock data")
    parser.add_argument("--output", default=None, help="Output format (json)")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    
    args = parser.parse_args()
    
    if args.env and os.path.exists(args.env):
        from dotenv import load_dotenv
        load_dotenv(args.env)
        
    stripe_token = os.getenv("STRIPE_API_TOKEN")
    slack_token = os.getenv("SLACK_API_TOKEN")
    
    if args.dry_run:
        print("Running in dry-run mode...")
        data = [{"client": "MockClient", "mrr": 100, "activity_score": 5, "churn_risk": {"score": 70, "level": "MEDIUM", "recommendation": "Schedule Check-in"}}]
        if args.output == "json":
            print(json.dumps(data))
        else:
            generate_report(data)
        return

    if not stripe_token or not slack_token:
        print("Error: STRIPE_API_TOKEN and SLACK_API_TOKEN environment variables are required.")
        return

    subscriptions = fetch_stripe_subscriptions(stripe_token)
    channels = ["C123", "C456"] 
    for channel in channels:
        fetch_slack_activity(slack_token, channel)
        
    data = []
    for sub in subscriptions:
        client = sub.get("customer")
        mrr = sub.get("plan", {}).get("unit_amount", 0) / 100 
        result = calculate_churn_risk(mrr, 0.02, 5)
        data.append({
            "client": client,
            "mrr": mrr,
            "activity_score": 5,
            "churn_risk": result,
            "recommendation": result["recommendation"]
        })
        
    if args.output == "json":
        print(json.dumps(data))
    else:
        generate_report(data)

if __name__ == "__main__":
    main()
