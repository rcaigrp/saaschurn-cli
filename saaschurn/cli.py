import argparse
import os
import sys
import json
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_mrr, calculate_churn_risk
from saaschurn.reporter import generate_report

def main(args=None):
    parser = argparse.ArgumentParser(description='SaaSChurn-CLI: Automate SaaS client health reporting and churn prediction')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Skip API calls, use mock data')
    parser.add_argument('--output', choices=['json'], help='Export results as JSON to stdout')
    parser.add_argument('--env', type=str, default='.env', help='Path to .env file')
    
    parsed = parser.parse_args(args)
    
    if parsed.env:
        load_dotenv(parsed.env)
    
    stripe_token = os.environ.get('STRIPE_API_TOKEN')
    slack_token = os.environ.get('SLACK_API_TOKEN')
    
    if not stripe_token or not slack_token:
        print('Error: STRIPE_API_TOKEN and SLACK_API_TOKEN must be set.')
        sys.exit(1)
        
    if parsed.dry_run:
        print('Running in dry-run mode...')
        subscriptions = [
            {'id': 'sub_1', 'customer_name': 'Client A', 'current_plan': 'Pro', 'price': 100, 'quantity': 1},
            {'id': 'sub_2', 'customer_name': 'Client B', 'current_plan': 'Basic', 'price': 50, 'quantity': 1}
        ]
        slack_activity = {
            'Client A': {'messages_count': 100},
            'Client B': {'messages_count': 5}
        }
        client_names = ['Client A', 'Client B']
    else:
        client_names = ['Client A']
        subscriptions = fetch_stripe_data(stripe_token)
        slack_activity = fetch_slack_data(slack_token, client_names)
    
    mrr = calculate_mrr(subscriptions)
    results = calculate_churn_risk(mrr, slack_activity)
    
    if parsed.output == 'json':
        print(json.dumps(results, indent=2))
    else:
        generate_report(results)

if __name__ == '__main__':
    main()
