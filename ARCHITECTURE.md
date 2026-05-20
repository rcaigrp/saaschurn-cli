# SaaSChurn-CLI Architecture

## Module Breakdown
- **CLI (`cli.py`)**: Uses `argparse` for command-line handling. Orchestrates the flow: config validation -> data fetching -> churn calculation -> output formatting. Supports `--dry-run` to bypass real API calls and `--output json` to switch renderers.
- **Stripe Client (`stripe_client.py`)**: Wraps Stripe API calls. Returns structured subscription data. Gracefully handles exceptions and defaults to empty lists to prevent crashes.
- **Slack Client (`slack_client.py`)**: Fetches channel history using the Slack API. Filters messages by date and parses engagement metrics.
- **Churn Calculator (`churn_calculator.py`)**: Applies a linear scoring model combining MRR trends and Slack activity drops. Outputs a probability score (0.0-1.0) and actionable insights.

## Data Flow
1. CLI parses args and loads env vars.
2. `stripe_client` fetches subscriptions and calculates MRR.
3. `slack_client` fetches activity logs for associated channels.
4. `churn_calculator` merges metrics and computes churn probability.
5. Results are formatted via `rich` or exported as JSON.

## Testing Strategy
All external API calls are mocked using `responses` library. Tests verify:
- Correct env var loading
- Mocked API response parsing
- Churn score computation logic
- CLI output formatting
- Dry-run mode behavior
