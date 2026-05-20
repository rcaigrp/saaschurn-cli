# SaaSChurn-CLI

A Python CLI tool to automate SaaS client health reporting and churn prediction across Stripe and Slack.

## Features
- Fetches Stripe subscription data.
- Fetches Slack channel activity.
- Calculates churn risk scores.
- Outputs formatted terminal reports.

## Usage
```bash
python -m saaschurn.cli health --dry-run
python -m saaschurn.cli health --output json
```
