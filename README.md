# SaaSChurn CLI

A Python CLI tool to automate SaaS client health reporting and churn prediction across Stripe and Slack.

## Installation
```bash
pip install -e .
```

## Usage
```bash
# Dry-run mode (no API calls)
python -m saaschurn.cli health --dry-run

# Export to JSON
python -m saaschurn.cli health --output json
```

## Environment Variables
- `STRIPE_API_TOKEN`: Your Stripe API key.
- `SLACK_API_TOKEN`: Your Slack API token.

## Testing
```bash
pytest tests/ -v --cov=saaschurn
```

## Features
- Fetches active subscriptions and calculates MRR.
- Pulls Slack workspace activity logs for client channels.
- Computes churn probability score based on revenue decline and activity drop.
- Outputs a formatted rich terminal table with actionable insights.
- Supports dry-run mode and JSON export.
