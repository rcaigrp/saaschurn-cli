# SaaSChurn CLI

A Python CLI tool to automate SaaS client health reporting and churn prediction across Stripe and Slack.

## Installation
```bash
pip install -e .
```

## Usage
```bash
python -m saaschurn.cli health --dry-run
python -m saaschurn.cli health --output json
```

## Environment Variables
- `STRIPE_API_TOKEN`
- `SLACK_API_TOKEN`

## Testing
```bash
pytest tests/ -v --cov=saaschurn
```