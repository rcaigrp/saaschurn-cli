import argparse
import json
import os
import sys
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import calculate_churn_risk
from saaschurn.reporter import generate_report
from dotenv import load_dotenv


def run_command(args):
    """Core logic for CLI commands."""
    load_dotenv(args.env)

    stripe_key = os.getenv("STRIPE_API_KEY")
    slack_token = os.getenv("SLACK_API_TOKEN")

    if args.dry_run:
        # Mock data for dry run
        subscriptions = [
            {"customer": "client1", "plan": {"amount": 10000}},
            {"customer": "client2", "plan": {"amount": 500}},
            {"customer": "client3", "plan": {"amount": 5000}},
        ]
        activity = {"channel1": 100, "channel2": 5, "channel3": 50}

        mrr_data = StripeFetcher(stripe_key).calculate_mrr(subscriptions)
        data = []
        for client, mrr in mrr_data.items():
            ch_idx = int(client.replace("client", "")) - 1
            act = activity.get(f"channel{ch_idx + 1}", 0)
            risk = calculate_churn_risk(mrr, act)
            data.append({
                "client": client,
                "mrr": mrr,
                "activity_score": act,
                "risk_level": risk["risk_level"],
                "recommendation": risk["recommendation"]
            })

        if args.output == "json":
            print(json.dumps(data, indent=2))
        else:
            generate_report(data)
    else:
        if not stripe_key or not slack_token:
            print("Error: STRIPE_API_KEY and SLACK_API_TOKEN are required.")
            return

        stripe_fetcher = StripeFetcher(stripe_key)
        slack_fetcher = SlackFetcher(slack_token)

        subscriptions = stripe_fetcher.fetch_active_subscriptions()
        mrr_data = stripe_fetcher.calculate_mrr(subscriptions)

        # Map clients to channels
        channels = [f"channel{int(client.replace('client', ''))}" for client in mrr_data.keys()]
        activity = slack_fetcher.fetch_channel_activity(channels)

        data = []
        for client, mrr in mrr_data.items():
            ch_idx = int(client.replace("client", "")) - 1
            act = activity.get(f"channel{ch_idx + 1}", 0)
            risk = calculate_churn_risk(mrr, act)
            data.append({
                "client": client,
                "mrr": mrr,
                "activity_score": act,
                "risk_level": risk["risk_level"],
                "recommendation": risk["recommendation"]
            })

        if args.output == "json":
            print(json.dumps(data, indent=2))
        else:
            generate_report(data)


def main():
    parser = argparse.ArgumentParser(description="SaaS Churn CLI Tool")
    parser.add_argument("command", choices=["health"], help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Use mock data instead of API")
    parser.add_argument("--output", choices=["json"], help="Output format")
    parser.add_argument("--env", type=str, default=".env", help="Path to .env file")

    args = parser.parse_args()
    run_command(args)


if __name__ == "__main__":
    main()
