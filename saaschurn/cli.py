import argparse
import sys
import os
import json

from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_churn_report
from saaschurn.reporter import print_report

import dotenv
dotenv.load_dotenv()


def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI Tool')
    parser.add_argument('command', help='Command to run (e.g., health)', choices=['health'])
    parser.add_argument('--dry-run', action='store_true', help='Run with mock data')
    parser.add_argument('--output', choices=['json', 'terminal'], default='terminal', help='Output format')

    args = parser.parse_args()

    if args.command != 'health':
        print("Unknown command")
        return

    # Setup environment variables for auth
    if not args.dry_run:
        os.environ.setdefault('STRIPE_API_TOKEN', os.environ.get('STRIPE_API_TOKEN', ''))
        os.environ.setdefault('SLACK_API_TOKEN', os.environ.get('SLACK_API_TOKEN', ''))

    # Fetch data
    stripe_data = fetch_stripe_data(args.dry_run)
    slack_data = fetch_slack_data(args.dry_run)

    # Calculate churn
    report = calculate_churn_report(stripe_data, slack_data)

    # Output
    if args.output == 'json':
        print(json.dumps(report))
    else:
        print_report(report)


if __name__ == '__main__':
    main()
