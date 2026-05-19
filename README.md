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
- **Meetings Held**: 1
- **Meetings Left**: 4
- **Status**: Active

## Completed Work
- Created `main.py` with core logic for auth, fetching, calculation, and reporting.
- Created `acceptance_tests.py` with mocked tests for all acceptance criteria.

## Test Results
- Tests defined and ready for execution.

## Known Bugs
- None.

## Next Steps
- Run acceptance tests to validate implementation.
- Fix any failing tests.
- Implement dry-run mode and JSON export enhancements if needed.
