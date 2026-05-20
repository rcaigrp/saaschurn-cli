#!/usr/bin/env python3
"""SaaSChurn CLI - Entry point and argument parsing"""
import argparse
import sys
import os
import json

from dotenv import load_dotenv

from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


def load_env_file(path):
    """Load environment variables from .env file."""
    if path and os.path.exists(path):
        load_dotenv(path)
        return True
    return False


def setup_parser():
    """Setup argparse CLI interface."""
    parser = argparse.ArgumentParser(description='SaaSChurn CLI - Health reporting and churn prediction')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Skip API calls, use mock data')
    parser.add_argument('--output', choices=['json'], default=None, help='Output format')
    parser.add_argument('--env', default=None, help='Path to .env file')
    return parser


def fetch_data(dry_run=False):
    """Fetch Stripe and Slack data."""
    if dry_run:
        # Mock data for dry-run
        stripe_subs = [
            {'id': 'sub_1', 'customer': 'cus_1', 'status': 'active', 'plan': {'unit_amount': 1000, 'currency': 'usd'}},
            {'id': 'sub_2', 'customer': 'cus_2', 'status': 'active', 'plan': {'unit_amount': 2000, 'currency': 'usd'}},
        ]
        slack_data = {
            'channel_1': {'message_count': 50, 'days': 30},
            'channel_2': {'message_count': 10, 'days': 30},
        }
        return stripe_subs, slack_data

    # Real API calls
    stripe_fetcher = StripeFetcher()
    slack_fetcher = SlackFetcher()

    stripe_subs = stripe_fetcher.get_active_subscriptions()
    slack_data = slack_fetcher.get_all_channel_activity()

    return stripe_subs, slack_data


def process_data(stripe_subs, slack_data):
    """Process data and calculate churn risk."""
    calculator = ChurnCalculator()
    results = []

    for sub in stripe_subs:
        customer_id = sub['customer']
        mrr = sub['plan']['unit_amount'] / 100  # Convert from cents

        # Find Slack channel for this customer
        channel_key = f'channel_{customer_id}'
        slack_info = slack_data.get(channel_key, {'message_count': 0, 'days': 30})

        # Calculate metrics
        mrr_decline = 0  # Would need historical data for this
        slack_activity_drop = 100 if slack_info['message_count'] < 10 else 0

        result = calculator.calculate_risk(mrr_decline, slack_activity_drop)

        results.append({
            'client': f'Customer_{customer_id}',
            'mrr': mrr,
            'activity_score': slack_info['message_count'],
            'risk_score': result['risk_score'],
            'recommendation': result['recommendation']
        })

    return results


def run_health_command(dry_run=False, output_format=None):
    """Run the health command."""
    stripe_subs, slack_data = fetch_data(dry_run)
    results = process_data(stripe_subs, slack_data)

    if output_format == 'json':
        Reporter().print_json(results)
    else:
        Reporter().print_table(results)


def main():
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    # Load env file if specified
    if args.env:
        load_env_file(args.env)

    if args.command == 'health':
        run_health_command(dry_run=args.dry_run, output_format=args.output)
    else:
        print(f'Unknown command: {args.command}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
