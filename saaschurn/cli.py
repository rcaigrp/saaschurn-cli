import argparse
import json
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import ChurnReporter

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument("command", choices=["health"], help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Use mock data")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal", help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")
    
    args = parser.parse_args()
    load_dotenv(args.env)
    
    if args.command == "health":
        if args.dry_run:
            print("Running in dry-run mode...")
            mock_data = {
                "subscriptions": [
                    {"id": "cus_1", "customer_name": "Acme Corp", "mrr": 500.0, "status": "active"},
                    {"id": "cus_2", "customer_name": "Globex", "mrr": 200.0, "status": "active"}
                ],
                "slack_activity": {
                    "#acme-corp": 100,
                    "#globex": 10
                }
            }
            results = process_data(mock_data)
        else:
            stripe_fetcher = StripeFetcher()
            slack_fetcher = SlackFetcher()
            subscriptions = stripe_fetcher.fetch_subscriptions()
            slack_activity = slack_fetcher.fetch_activity()
            results = process_data({"subscriptions": subscriptions, "slack_activity": slack_activity})
        
        if args.output == "json":
            print(json.dumps(results, indent=2))
        else:
            reporter = ChurnReporter()
            reporter.print_report(results)

def process_data(data):
    calc = ChurnCalculator(data["subscriptions"], data["slack_activity"])
    return calc.calculate_risk_scores()

if __name__ == "__main__":
    main()
