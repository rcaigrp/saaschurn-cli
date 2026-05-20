# SaaSChurn-CLI

## Goal
Build a Python CLI tool (SaaSChurn-CLI) that authenticates via environment variables for Stripe and Slack API tokens. It fetches active subscriptions, calculates MRR, pulls Slack workspace activity logs for associated client channels, and computes a churn probability score based on revenue decline and activity drop. Outputs a formatted `rich` terminal table with actionable insights. Supports dry-run mode and JSON export.

## Acceptance Criteria
- Authenticate via environment variables for Stripe and Slack API tokens.
- Fetch active subscriptions from Stripe and calculate MRR.
- Pull Slack workspace activity logs for associated client channels.
- Compute a churn probability score based on revenue decline and activity drop.
- Output a formatted `rich` terminal table with actionable insights.
- Support dry-run mode and JSON export.

## Sprint Status
- **Meetings Held**: 2
- **Meetings Left**: 3
- **Status**: Active

## Completed Work
- Created `main.py` with core logic for auth, fetching, calculation, and reporting.
- Created `acceptance_tests.py` with mocked tests for all acceptance criteria.
- Implemented `fetchers.py` with Stripe pagination and rate limit handling.
- Implemented `calculators.py` for MRR and churn risk scoring.
- Implemented `reporter.py` with `rich` terminal formatting.
- Created `saaschurn/cli.py` with argparse, dry-run, and JSON export support.

## Test Results
- Running acceptance tests now...

## Known Bugs
- None.

## Next Steps
- Fix any failing tests.
- Implement dry-run mode and JSON export enhancements if needed.