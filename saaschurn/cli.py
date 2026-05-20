import argparse
import os
import json
import sys
from dotenv import load_dotenv
from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", choices=["json", "terminal"], default="terminal")
    parser.add_argument("--env", type=str, default=".env")
    
    args = parser.parse_args()
    
    load_dotenv(args.env)
    
    stripe_data = fetch_stripe_data(dry_run=args.dry_run)
    slack_data = fetch_slack_data(dry_run=args.dry_run)
    
    results = {}
    for sub_id, sub_info in stripe_data.items():
        mrr = sub_info['mrr']
        slack_msgs = slack_data.get(sub_id, {}).get('messages', 0)
        risk_score, risk_level = calculate_churn_risk(mrr, mrr_decline_rate=0, slack_messages=slack_msgs)
        
        results[sub_id] = {
            'mrr': mrr,
            'activity': slack_msgs,
            'risk_score': risk_score,
            'risk_level': risk_level
        }
        
    generate_report(results, output_json=args.output == 'json')

if __name__ == '__main__':
    main()
