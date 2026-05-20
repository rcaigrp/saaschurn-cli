import argparse
import sys
from stripe_client import fetch_active_subscriptions
from mrr_calculator import calculate_mrr
from exporter import export_to_json

def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI')
    parser.add_argument('--api-key', required=True, help='Stripe API Key')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--dry-run', action='store_true', help='Simulate without saving')
    
    args = parser.parse_args()
    
    subscriptions = fetch_active_subscriptions(args.api_key)
    mrr = calculate_mrr(subscriptions)
    
    print(f"Total MRR: ${mrr}")
    
    if not args.dry_run and args.output:
        export_to_json(subscriptions, mrr, args.output)
        print(f"Data exported to {args.output}")

if __name__ == '__main__':
    main()
