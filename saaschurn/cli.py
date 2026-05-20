import argparse
import json
import sys
from saaschurn.fetchers import fetch_stripe_subscriptions, fetch_slack_activity
from saaschurn.calculators import calculate_mrr, calculate_churn_risk
from saaschurn.reporter import generate_report


def main():
    parser = argparse.ArgumentParser(description='SaaS Churn CLI Tool')
    parser.add_argument('command', choices=['health'], help='Command to run')
    parser.add_argument('--dry-run', action='store_true', help='Use mock data')
    parser.add_argument('--output', choices=['json'], help='Output format')
    parser.add_argument('--env', type=str, default='.env', help='Path to .env file')

    args = parser.parse_args()

    if args.command == 'health':
        if args.dry_run:
            stripe_data = [
                {"id": "sub_1", "customer": "client_1", "status": "active", "plan": {"unit_amount": 1000}, "current_period_end": 1700000000},
                {"id": "sub_2", "customer": "client_2", "status": "active", "plan": {"unit_amount": 2000}, "current_period_end": 1700000000}
            ]
            slack_data = {"client_1": 10, "client_2": 5}
        else:
            import os
            from dotenv import load_dotenv
            load_dotenv(args.env)
            stripe_token = os.getenv('STRIPE_API_KEY')
            slack_token = os.getenv('SLACK_API_KEY')
            stripe_data = fetch_stripe_subscriptions(stripe_token)
            slack_data = fetch_slack_activity(slack_token)

        clients = []
        for sub in stripe_data:
            client_id = sub.get('customer')
            mrr = calculate_mrr(sub)
            activity = slack_data.get(client_id, 0)
            risk_score = calculate_churn_risk(mrr, activity)
            risk_level = 'LOW' if risk_score < 30 else ('MEDIUM' if risk_score <= 70 else 'HIGH')
            recommendation = 'No action needed' if risk_level == 'LOW' else ('Review engagement' if risk_level == 'MEDIUM' else 'Immediate outreach required')
            clients.append({
                "client": client_id,
                "mrr": mrr,
                "activity_score": activity,
                "churn_risk": risk_score,
                "recommendation": recommendation
            })

        if args.output == 'json':
            print(json.dumps(clients, indent=2))
        else:
            generate_report(clients)

if __name__ == '__main__':
    main()
