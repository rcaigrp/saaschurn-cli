import argparse
import json
import os
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_mrr, calculate_churn_risk, get_risk_level
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument('command', help='Command to run (health)', default='health')
    parser.add_argument('--dry-run', action='store_true', help='Use mock data')
    parser.add_argument('--output', choices=['json'], help='Output format')
    parser.add_argument('--env', default='.env', help='Env file')
    
    args = parser.parse_args()
    
    if args.env:
        from dotenv import load_dotenv
        load_dotenv(args.env)
        
    stripe_token = os.environ.get('STRIPE_API_KEY')
    slack_token = os.environ.get('SLACK_API_TOKEN')
    
    if args.dry_run:
        subscriptions = [
            {"plan": {"amount": 10000}, "customer_name": "Client A", "customer_id": "cus_1"},
            {"plan": {"amount": 500}, "customer_name": "Client B", "customer_id": "cus_2"}
        ]
        activity = {"cus_1": 20, "cus_2": 5}
    else:
        if not stripe_token or not slack_token:
            print("Error: Missing API tokens in environment.")
            return
        subscriptions = fetch_stripe_subscriptions(stripe_token)
        channels = fetch_slack_activity(slack_token)
        # This is a simplified approach for CLI
        activity = {}
    
    results = []
    for sub in subscriptions:
        client = sub.get('customer_name', 'Unknown')
        mrr = calculate_mrr([sub])
        client_id = sub.get('customer_id', 'unknown')
        act_score = activity.get(client_id, 0)
        risk = calculate_churn_risk(mrr, act_score)
        rec = "High Engagement" if risk < 30 else "Monitor"
        
        results.append({
            'client': client,
            'mrr': mrr,
            'activity': act_score,
            'risk': risk,
            'recommendation': rec
        })
    
    if args.output == 'json':
        return json.dumps(results)
    else:
        generate_report(results)
        return None

if __name__ == '__main__':
    main()