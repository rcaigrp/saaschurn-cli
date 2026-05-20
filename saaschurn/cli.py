import argparse
import json
import sys
import os
from dotenv import load_dotenv
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import calculate_mrr, calculate_churn_risk, get_risk_level, get_recommendation
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Use mock data")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal", help="Output format")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    
    args = parser.parse_args()
    
    load_dotenv(args.env)
    
    stripe_token = os.environ.get("STRIPE_API_TOKEN")
    slack_token = os.environ.get("SLACK_API_TOKEN")
    
    if not stripe_token or not slack_token:
        print("Missing environment variables: STRIPE_API_TOKEN or SLACK_API_TOKEN")
        sys.exit(1)
        
    if args.dry_run:
        data = [
            {"client": "DryRunClient", "mrr": 15.0, "activity_score": 80, "churn_risk": 40, "recommendation": "Monitor"}
        ]
    else:
        stripe = StripeFetcher(stripe_token)
        slack = SlackFetcher(slack_token)
        
        subs = stripe.fetch_active_subscriptions()
        client_data = []
        for sub in subs:
            client_id = sub.get("customer", "unknown")
            mrr = calculate_mrr(sub.get("plan", {}).get("unit_amount", 0))
            slack_msgs = slack.fetch_channel_activity(f"C_{client_id}")
            activity_score = max(0, min(100, slack_msgs))
            mrr_decline = 0
            slack_drop = 100 if slack_msgs > 10 else 50
            risk = calculate_churn_risk(mrr_decline, slack_drop)
            level = get_risk_level(risk)
            rec = get_recommendation(level)
            client_data.append({
                "client": client_id,
                "mrr": mrr,
                "activity_score": activity_score,
                "churn_risk": risk,
                "recommendation": rec
            })
            
    if args.output == "json":
        print(json.dumps(client_data))
    else:
        generate_report(client_data)

if __name__ == "__main__":
    main()
