"""CLI interface for SaaSChurn."""
import argparse
import json
import sys
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter


def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI Tool')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Use mock data instead of API calls')
    parser.add_argument('--output', choices=['json'], help='Export results as JSON')
    
    args = parser.parse_args()
    
    if args.command == 'health':
        fetcher = StripeFetcher()
        slack_fetcher = SlackFetcher()
        calculator = ChurnCalculator()
        reporter = Reporter()
        
        # Fetch data
        if args.dry_run:
            subscriptions = fetcher.get_mock_subscriptions()
            slack_activity = slack_fetcher.get_mock_activity()
        else:
            try:
                subscriptions = fetcher.get_active_subscriptions()
                slack_activity = slack_fetcher.get_channel_activity()
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        
        # Calculate churn
        results = calculator.calculate_risk(subscriptions, slack_activity)
        
        # Output
        if args.output == 'json':
            print(json.dumps(results))
        else:
            reporter.print_table(results)


if __name__ == '__main__':
    main()
