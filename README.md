# SaaSChurn-CLI

## Goal
Build a Python CLI tool to detect SaaS churn by analyzing Stripe subscriptions.

## Acceptance Criteria
1. Fetch active subscriptions from Stripe API.
2. Calculate Monthly Recurring Revenue (MRR).
3. Export data to JSON.
4. CLI interface with argument parsing.

## Files
- saaschurn/__init__.py
- saaschurn/stripe_client.py
- acceptance_tests.py