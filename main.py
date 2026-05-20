import os
import sys
import json
import argparse
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def get_env_var(name):
    val = os.getenv(name)
    if not val:
        console.print(f"[red]Error: {name} environment variable is not set.[/red]")
        sys.exit(1)
    return val

def fetch_stripe_subscriptions(token, dry_run=False):
    if dry_run:
        return [
            {"id": "sub_1", "customer_name": "ClientA", "status": "active", "current_period_end": 1700000000, "quantity": 1, "price": {"amount": 10000}},
            {"id": "sub_2", "customer_name": "ClientB", "status": "active", "current_period_end": 1700000000, "quantity": 2, "price": {"amount": 5000}},
        ]
    url = "https://api.stripe.com/v1/subscriptions"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()["data"]
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Stripe API Error: {e}[/red]")
        return []

def calculate_mrr(subscriptions):
    mrr_data = {}
    for sub in subscriptions:
        if sub.get("status") != "active":
            continue
        name = sub.get("customer_name", "Unknown")
        price = sub.get("price", {}).get("amount", 0)
        quantity = sub.get("quantity", 1)
        mrr = (price * quantity) / 100
        mrr_data[name] = mrr
    return mrr_data

def fetch_slack_activity(token, dry_run=False):
    if dry_run:
        return {"ClientA": 15, "ClientB": 5}
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    activity = {}
    # In a real scenario, we'd need to know which channels belong to which client.
    # Here we assume a mapping or fetch all channels.
    # For simplicity, we mock the channel list or assume predefined clients.
    clients = ["ClientA", "ClientB"] # This would be dynamic in production
    for client in clients:
        channel = f"#{client}"
        payload = {"channel": channel}
        try:
            resp = requests.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            msg_count = len(data.get("messages", []))
            activity[client] = msg_count
        except requests.exceptions.RequestException as e:
            console.print(f"[red]Slack API Error for {client}: {e}[/red]")
            activity[client] = 0
    return activity

def calculate_churn_risk(mrr_data, activity_data):
    risk_scores = {}
    for client, mrr in mrr_data.items():
        base_score = 50
        # MRR decline logic: if MRR is low, risk increases
        if mrr < 50:
            base_score += 30
        # Slack activity logic: low activity increases risk
        msgs = activity_data.get(client, 0)
        if msgs < 10:
            base_score += 20
        risk_scores[client] = min(base_score, 100)
    return risk_scores

def generate_report(mrr_data, activity_data, risk_scores, dry_run=False):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Client", style="bold")
    table.add_column("MRR")
    table.add_column("Activity")
    table.add_column("Risk")
    table.add_column("Recommendation")

    for client, mrr in mrr_data.items():
        risk = risk_scores.get(client, 0)
        activity = activity_data.get(client, 0)
        if risk > 70:
            color = "red"
            rec = "Immediate outreach required"
        elif risk > 30:
            color = "yellow"
            rec = "Schedule check-in"
        else:
            color = "green"
            rec = "No action needed"
        table.add_row(client, f"${mrr:.2f}", str(activity), str(risk), rec, style=color)
    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="SaaSChurn CLI")
    parser.add_argument("command", help="Command to run")
    parser.add_argument("--dry-run", action="store_true", help="Use mock data")
    parser.add_argument("--output", choices=["json"], default=None, help="Export to JSON")
    args = parser.parse_args()

    if args.command == "health":
        stripe_token = get_env_var("STRIPE_API_KEY")
        slack_token = get_env_var("SLACK_API_TOKEN")

        subscriptions = fetch_stripe_subscriptions(stripe_token, dry_run=args.dry_run)
        mrr_data = calculate_mrr(subscriptions)
        activity_data = fetch_slack_activity(slack_token, dry_run=args.dry_run)
        risk_scores = calculate_churn_risk(mrr_data, activity_data)

        if args.output == "json":
            output = {"mrr": mrr_data, "activity": activity_data, "risk": risk_scores}
            print(json.dumps(output))
        else:
            generate_report(mrr_data, activity_data, risk_scores, args.dry_run)

if __name__ == "__main__":
    main()
