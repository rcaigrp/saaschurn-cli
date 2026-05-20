import argparse
import os
import json
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_mrr, calculate_activity_score, calculate_churn_risk
from saaschurn.reporter import print_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    subparsers = parser.add_subparsers(dest="command")
    health_parser = subparsers.add_parser("health")
    health_parser.add_argument("--dry-run", action="store_true")
    health_parser.add_argument("--output", choices=["json", "terminal"])
    
    args = parser.parse_args()
    
    if args.command == "health":
        if args.dry_run:
            print("Dry run mode: skipping API calls.")
            results = [{"client": "Mock Client", "mrr": 1000, "activity_score": 50, "churn_risk": 50}]
        else:
            stripe_token = os.getenv("STRIPE_API_TOKEN")
            slack_token = os.getenv("SLACK_API_TOKEN")
            if not stripe_token or not slack_token:
                print("Error: Missing STRIPE_API_TOKEN or SLACK_API_TOKEN")
                return
            
            subscriptions = fetch_stripe_subscriptions(stripe_token)
            slack_activity = fetch_slack_activity(slack_token, ["C0123456789"])
            
            mrr = calculate_mrr(subscriptions)
            activity_score = calculate_activity_score(slack_activity.get("C0123456789", 0))
            churn_risk = calculate_churn_risk(mrr, activity_score)
            
            results = [{"client": "Client A", "mrr": mrr, "activity_score": activity_score, "churn_risk": churn_risk}]
        
        if args.output == "json":
            print(json.dumps(results))
        else:
            print_report(results)

if __name__ == "__main__":
    main()