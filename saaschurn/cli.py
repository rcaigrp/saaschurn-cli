import argparse
import json
import os
import sys
from datetime import datetime

from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import ReportGenerator


def load_env_file(env_path):
    """Load environment variables from .env file."""
    if os.path.exists(env_path):
        from dotenv import load_dotenv
        load_dotenv(env_path)
    # Check for required env vars
    if not os.environ.get('STRIPE_API_KEY'):
        print("Error: STRIPE_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)
    if not os.environ.get('SLACK_API_TOKEN'):
        print("Error: SLACK_API_TOKEN not set in environment", file=sys.stderr)
        sys.exit(1)


def setup_parser():
    """Set up argument parser."""
    parser = argparse.ArgumentParser(description='SaaS Churn CLI Tool')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Use mock data instead of API calls')
    parser.add_argument('--output', choices=['json', 'terminal'], default='terminal', help='Output format')
    parser.add_argument('--env', default='.env', help='Path to .env file')
    return parser


def main():
    """Main entry point."""
    parser = setup_parser()
    args = parser.parse_args()

    # Load env file
    load_env_file(args.env)

    if args.command == 'health':
        if args.dry_run:
            # Use mock data
            data = get_mock_data()
            results = process_data(data)
        else:
            # Fetch real data
            stripe_fetcher = StripeFetcher(os.environ['STRIPE_API_KEY'])
            slack_fetcher = SlackFetcher(os.environ['SLACK_API_TOKEN'])
            data = fetch_real_data(stripe_fetcher, slack_fetcher)
            results = process_data(data)

        # Generate output
        if args.output == 'json':
            print(json.dumps(results, indent=2))
        else:
            gen = ReportGenerator(results)
            gen.generate_report()


def get_mock_data():
    """Return mock data for dry-run mode."""
    return {
        'subscriptions': [
            {'customer_name': 'Acme Corp', 'mrr': 1000, 'previous_mrr': 1100, 'channel': 'acme-corp-channel'},
            {'customer_name': 'Globex Inc', 'mrr': 500, 'previous_mrr': 500, 'channel': 'globex-inc-channel'},
            {'customer_name': 'Initech', 'mrr': 200, 'previous_mrr': 300, 'channel': 'initech-channel'}
        ],
        'slack_activity': {
            'acme-corp-channel': {'total_messages': 100, 'days': 30},
            'globex-inc-channel': {'total_messages': 50, 'days': 30},
            'initech-channel': {'total_messages': 5, 'days': 30}
        }
    }


def fetch_real_data(stripe_fetcher, slack_fetcher):
    """Fetch data from real APIs."""
    subscriptions = stripe_fetcher.get_active_subscriptions()\n    slack_activity = slack_fetcher.get_channel_activity()
    return {'subscriptions': subscriptions, 'slack_activity': slack_activity}


def process_data(data):
    """Process data and calculate churn risk."""
    calculator = ChurnCalculator()
    results = []
    for sub in data['subscriptions']:
        risk = calculator.calculate_risk(sub)
        results.append(risk)
    return results


if __name__ == '__main__':
    main()
