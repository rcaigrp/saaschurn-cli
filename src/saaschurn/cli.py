import argparse
import json
import os
import sys
from dotenv import load_dotenv

from .fetchers import fetch_stripe_data, fetch_slack_data
from .calculators import calculate_churn_risk
from .reporter import generate_report


def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI Tool')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Skip API calls')
    parser.add_argument('--output', choices=['json'], help='Output format')
    parser.add_argument('--env', type=str, default='.env', help='Path to env file')
    
    args = parser.parse_args()
    load_dotenv(args.env)
    
    if args.command == 'health':
        if args.dry_run:
            stripe_data = []
            slack_data = {}
        else:
            stripe_data = fetch_stripe_data()
            slack_data = fetch_slack_data()
            
        results = calculate_churn_risk(stripe_data, slack_data)
        
        if args.output == 'json':
            print(json.dumps(results))
        else:
            generate_report(results)


if __name__ == '__main__':
    main()
