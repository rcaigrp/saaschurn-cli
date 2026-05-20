import argparse
import os
import sys
import json
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_mrr, calculate_churn_score
from saaschurn.reporter import generate_report

def main(argv=None):
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["json"])
    
    args = parser.parse_args(argv)
    
    if args.dry_run:
        data = [{"client": "MockClient", "mrr": 1000, "risk": "LOW", "rec": "Keep engaging"}]
    else:
        stripe_token = os.getenv("STRIPE_API_TOKEN")
        slack_token = os.getenv("SLACK_API_TOKEN")
        if not stripe_token or not slack_token:
            print("Error: Missing env vars", file=sys.stderr)
            sys.exit(1)
        
        stripe_data = fetch_stripe_subscriptions(stripe_token)
        slack_data = fetch_slack_activity(slack_token)
        
        mrr = calculate_mrr(stripe_data)
        score = calculate_churn_score(mrr, slack_data)
        data = [{"client": "RealClient", "mrr": mrr, "risk": "MEDIUM", "rec": "Investigate"}]

    if args.output == "json":
        print(json.dumps(data))
    else:
        generate_report(data)

if __name__ == "__main__":
    main()
