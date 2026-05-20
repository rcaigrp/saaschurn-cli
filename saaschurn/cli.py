import argparse
import json
import sys
from saaschurn.fetchers import fetch_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report

def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI')
    parser.add_argument('command', choices=['health'])
    parser.add_argument('--dry-run', action='store_true', help='Use mock data instead of API calls')
    parser.add_argument('--output', choices=['json'], help='Export results as JSON')
    args = parser.parse_args()

    if args.command == 'health':
        if args.dry_run:
            print("Running in dry-run mode...")
            subscriptions = {"cust_1": 1000.0, "cust_2": 500.0}
            slack_activity = {"cust_1": 100, "cust_2": 5}
        else:
            subscriptions = fetch_subscriptions()
            slack_activity = fetch_slack_activity()

        results = calculate_churn_risk(subscriptions, slack_activity)

        if args.output == 'json':
            print(json.dumps(results, indent=2))
        else:
            generate_report(results)

if __name__ == '__main__':
    main()