import argparse
import json
import os
import sys
from dotenv import load_dotenv

from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI Tool')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Use mock data instead of real API calls')
    parser.add_argument('--output', choices=['json'], help='Export results as JSON')
    parser.add_argument('--env', type=str, default='.env', help='Path to .env file')

    args = parser.parse_args()

    # Load environment variables
    load_dotenv(args.env)

    # Initialize fetchers
    stripe_key = os.getenv('STRIPE_API_KEY')
    slack_token = os.getenv('SLACK_API_TOKEN')

    if not stripe_key or not slack_token:
        print('Error: STRIPE_API_KEY and SLACK_API_TOKEN environment variables are required.', file=sys.stderr)
        sys.exit(1)

    stripe_fetcher = StripeFetcher(api_key=stripe_key)
    slack_fetcher = SlackFetcher(token=slack_token)

    # Process data
    if args.dry_run:
        print('Running in dry-run mode with mock data...')
        stripe_data = stripe_fetcher.fetch_mock()
        slack_data = slack_fetcher.fetch_mock()
    else:
        stripe_data = stripe_fetcher.fetch()
        slack_data = slack_fetcher.fetch()

    # Calculate churn risk
    calculator = ChurnCalculator()
    results = calculator.calculate(stripe_data, slack_data)

    # Generate report
    reporter = Reporter()

    if args.output == 'json':
        print(json.dumps(results, indent=2))
    else:
        reporter.print_table(results)


if __name__ == '__main__':
    main()
