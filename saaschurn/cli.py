import argparse
import json
import os
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Run with mock data')
    parser.add_argument('--output', choices=['json'], help='Output format')
    parser.add_argument('--env', default='.env', help='Path to .env file')
    
    args = parser.parse_args()
    
    if os.path.exists(args.env):
        load_dotenv(args.env)
        
    if args.dry_run:
        stripe_data = [
            {'customer_id': 'cus_1', 'plan_id': 'plan_1', 'status': 'active', 'plan': {'amount': 10000}},
            {'customer_id': 'cus_2', 'plan_id': 'plan_2', 'status': 'past_due', 'plan': {'amount': 5000}},
        ]
        slack_data = {'cus_1': 50, 'cus_2': 2}
    else:
        stripe_api_key = os.getenv('STRIPE_API_KEY')
        slack_token = os.getenv('SLACK_API_TOKEN')
        stripe_data = fetch_stripe_subscriptions(stripe_api_key)
        channels = [s.get('customer_id') for s in stripe_data]
        slack_data = fetch_slack_activity(slack_token, channels)
        
    results = calculate_churn_risk(stripe_data, slack_data)
    
    if args.output == 'json':
        print(json.dumps(results, indent=2))
    else:
        generate_report(results)

if __name__ == '__main__':
    main()
