import argparse
import sys
import os

from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report

def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['health'])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--output', choices=['json', 'table'], default='table')
    args = parser.parse_args()

    if args.command == 'health':
        if args.dry_run:
            stripe_data = [{'customer': 'cus_1', 'plan': {'amount': 10000}}]
            slack_data = []
        else:
            stripe_data = fetch_stripe_data()
            slack_data = fetch_slack_data()
        results = calculate_churn_risk(stripe_data, slack_data)
        generate_report(results, dry_run=args.dry_run, output_format=args.output)
    else:
        print("Unknown command")
        sys.exit(1)

if __name__ == '__main__':
    main()
