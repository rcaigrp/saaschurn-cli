import argparse
import os
import json
import sys
from saaschurn import fetchers
from saaschurn import calculators
from saaschurn import reporter

def main():
    parser = argparse.ArgumentParser(description="SaaSChurn CLI")
    parser.add_argument("command", choices=["health"])
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls, use mock data")
    parser.add_argument("--output", choices=["json"], help="Export results as JSON")
    args = parser.parse_args()
    stripe_key = os.environ.get("STRIPE_API_KEY")
    slack_token = os.environ.get("SLACK_API_TOKEN")
    if not args.dry_run:
        if not stripe_key:
            print("Error: STRIPE_API_KEY not set")
            sys.exit(1)
        if not slack_token:
            print("Error: SLACK_API_TOKEN not set")
            sys.exit(1)
        stripe_data = fetchers.fetch_stripe_data(stripe_key)
        channels = ["channel_1", "channel_2"]
        slack_data = fetchers.fetch_slack_data(slack_token, channels)
        results = []
        for sub in stripe_data:
            act_score = sum(slack_data.get(ch, 0) for ch in channels) / len(channels) if channels else 0
            risk_score, risk_level = calculators.calculate_churn_risk(sub["mrr"], 0, act_score)
            results.append({
                "client": sub["customer"],
                "mrr": sub["mrr"],
                "activity_score": act_score,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": f"Monitor closely ({risk_level})"
            })
    else:
        results = []
        for sub in fetchers.get_mock_stripe_data():
            act_score = 50 if "channel_1" in fetchers.get_mock_slack_data() else 0
            risk_score, risk_level = calculators.calculate_churn_risk(sub["mrr"], 0, act_score)
            results.append({
                "client": sub["customer"],
                "mrr": sub["mrr"],
                "activity_score": act_score,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "recommendation": f"Monitor closely ({risk_level})"
            })
    if args.output == "json":
        print(json.dumps(results))
    else:
        reporter.generate_report(results)

if __name__ == "__main__":
    main()
