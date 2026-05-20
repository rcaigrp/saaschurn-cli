import os
import time
import requests
from typing import Dict, List, Optional


def _fetch_with_backoff(url: str, headers: dict, max_retries: int = 3) -> dict:
    """Fetch URL with exponential backoff for rate limits."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 429:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return {}
    return {}


def fetch_stripe_data(dry_run: bool = False) -> List[dict]:
    """Fetch active Stripe subscriptions and calculate MRR.
    
    Args:
        dry_run: If True, use mock data instead of API calls.
        
    Returns:
        List of subscription data with client info and MRR.
    """
    if dry_run:
        return [
            {"client": "Acme Corp", "stripe_id": "sub_001", "mrr": 1000.0, "previous_mrr": 1100.0},
            {"client": "Globex Inc", "stripe_id": "sub_002", "mrr": 500.0, "previous_mrr": 550.0},
            {"client": "Initech", "stripe_id": "sub_003", "mrr": 2000.0, "previous_mrr": 2000.0},
        ]
    
    stripe_token = os.environ.get('STRIPE_API_TOKEN')
    if not stripe_token:
        raise ValueError("STRIPE_API_TOKEN environment variable not set")
    
    headers = {"Authorization": f"Bearer {stripe_token}"}
    url = "https://api.stripe.com/v1/subscriptions"
    subscriptions = []
    next_url = url
    
    while next_url:
        params = {"limit": 100}
        response_data = _fetch_with_backoff(next_url, headers)
        if not response_data:
            break
            
        if "data" in response_data:
            subscriptions.extend(response_data["data"])
        
        # Check for pagination
        if "next" in response_data:
            next_url = response_data["next"]
        else:
            next_url = None
    
    # Process subscriptions into client data
    client_data = {}
    for sub in subscriptions:
        if sub.get("status") == "active":
            customer_id = sub.get("customer", "")
            if customer_id not in client_data:
                client_data[customer_id] = {
                    "client": sub.get("metadata", {}).get("client_name", customer_id),
                    "stripe_id": customer_id,
                    "mrr": 0.0,
                    "previous_mrr": 0.0
                }
            
            # Calculate MRR from subscription
            price = sub.get("items", {}).get("data", [{}])[0].get("price", {})
            if price:
                amount = price.get("amount", 0)
                recurring = price.get("recurring", {})
                if recurring:
                    interval = recurring.get("interval", "month")
                    if interval == "month":
                        client_data[customer_id]["mrr"] += amount / 100
                    elif interval == "year":
                        client_data[customer_id]["mrr"] += amount / 1200
                    else:
                        client_data[customer_id]["mrr"] += amount / 100
    
    return list(client_data.values())


def fetch_slack_data(dry_run: bool = False) -> Dict[str, dict]:
    """Fetch Slack channel activity and aggregate message counts.
    
    Args:
        dry_run: If True, use mock data instead of API calls.
        
    Returns:
        Dict mapping client names to their activity data.
    """
    if dry_run:
        return {
            "Acme Corp": {"channel": "acme-corp", "message_count": 150, "days_active": 25, "avg_msgs_per_day": 6.0},
            "Globex Inc": {"channel": "globex-inc", "message_count": 30, "days_active": 10, "avg_msgs_per_day": 3.0},
            "Initech": {"channel": "initech", "message_count": 200, "days_active": 30, "avg_msgs_per_day": 6.7},
        }
    
    slack_token = os.environ.get('SLACK_API_TOKEN')
    if not slack_token:
        raise ValueError("SLACK_API_TOKEN environment variable not set")
    
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # Get all channels first
    channels_url = "https://slack.com/api/conversations.list"
    channels_response = _fetch_with_backoff(channels_url, headers)
    channels = channels_response.get("channels", []) if channels_response else []
    
    # Map client names to channels (this would normally be done via a mapping)
    # For now, we'll use a simple client_name -> channel mapping
    client_channels = {
        "Acme Corp": "acme-corp",
        "Globex Inc": "globex-inc",
        "Initech": "initech"
    }
    
    slack_data = {}
    
    for client_name, channel_name in client_channels.items():
        try:
            # Find channel ID
            channel_id = None
            for ch in channels:
                if ch.get("name") == channel_name:
                    channel_id = ch.get("id")
                    break
            
            if not channel_id:
                # Channel not found, skip gracefully
                continue
            
            # Fetch channel history
            history_url = "https://slack.com/api/conversations.history"
            params = {"channel": channel_id, "limit": 100}
            
            message_count = 0
            days_active = set()
            next_url = history_url
            
            while next_url:
                params = {"channel": channel_id, "limit": 100}
                response_data = requests.get(next_url, headers=headers, params=params, timeout=10)
                
                if response_data.status_code == 200:
                    history = response_data.json()
                    if "messages" in history:
                        for msg in history["messages"]:
                            message_count += 1
                            if "ts" in msg:
                                # Extract day from timestamp
                                day = msg["ts"].split(".")[0]
                                days_active.add(day)
                    
                    if "next_cursor" in history:
                        next_url = f"{history_url}?cursor={history['next_cursor']}"
                    else:
                        next_url = None
                else:
                    next_url = None
            
            days_active_count = len(days_active) if days_active else 1
            avg_msgs = message_count / days_active_count if days_active_count > 0 else 0
            
            slack_data[client_name] = {
                "channel": channel_name,
                "message_count": message_count,
                "days_active": days_active_count,
                "avg_msgs_per_day": round(avg_msgs, 1)
            }
        except Exception:
            # Skip gracefully if channel or client not found
            continue
    
    return slack_data
