import argparse
import json
import os
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument("command", choices=["health"], help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls and use mock data")
    parser.add_argument("--output", choices=["json"], help="Output format")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    
    args = parser.parse_args()
    
    load_dotenv(args.env)
    
    if args.command == "health":
        if args.dry_run:
            stripe_data = {
                "subscriptions": [
                    {"id": "sub_1", "customer_id": "cus_1", "customer_name": "Acme Corp", "amount": 1000},
                    {"id": "sub_2", "customer_id": "cus_2", "customer_name": "Globex Inc", "amount": 2000},
                ]
            }
            slack_data = {
                "channels": [
                    {"name": "acme-general", "messages": 150},
                    {"name": "globex-support", "messages": 50},
                ]
            }
        else:
            stripe_token = os.getenv("STRIPE_API_KEY")
            slack_token = os.getenv("SLACK_API_TOKEN")
            if not stripe_token or not slack_token:
                print("Error: STRIPE_API_KEY and SLACK_API_TOKEN are required.")
                sys.exit(1)
            stripe_data = fetch_stripe_data(stripe_token)
            slack_data = fetch_slack_data(slack_token)
        
        clients = calculate_churn_risk(stripe_data, slack_data)
        
        if args.output == "json":
            print(json.dumps(clients, indent=2))
        else:
            generate_report(clients)

if __name__ == "__main__":
    main()
