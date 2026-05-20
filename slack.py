def fetch_activity_logs():
    """Pulls Slack workspace activity logs."""
    return [
        {"channel": "general", "messages": 100},
        {"channel": "support", "messages": 50}
    ]
