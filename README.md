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
- **Status**: Active (Redesigned)

## Completed Work
- Implemented `saaschurn/` package structure.
- Implemented `fetchers.py`, `calculators.py`, `reporter.py`, `cli.py`.
- Created comprehensive `acceptance_tests.py`.

## Test Results
- Pending execution.

## Known Bugs
- None (Redesign phase).

## Next Steps
- Run acceptance tests.
- Fix any failing tests.
