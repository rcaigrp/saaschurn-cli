import os
import time
import requests
from dotenv import load_dotenv


def load_env():
    """Load environment variables from .env file."""
    load_dotenv()
    stripe_key = os.getenv("STRIPE_API_KEY")
    slack_token = os.getenv("SLACK_APP_TOKEN")
    if not stripe_key or not slack_token:
        raise ValueError("Missing required environment variables: STRIPE_API_KEY, SLACK_APP_TOKEN")
    return stripe_key, slack_token


def fetch_stripe_data():
    """Fetch Stripe subscriptions with pagination and rate limit handling."""
    stripe_key, _ = load_env()
    headers = {"Authorization": f"Bearer {stripe_key}"}
    url = "https://api.stripe.com/v1/subscriptions"
    
    stripe_data = {}
    page = 0
    
    while True:
        try:
            # Add delay to handle rate limits
            if page > 0:
                time.sleep(1)
            
            response = requests.get(url, headers=headers)
            
            # Handle rate limits with exponential backoff
            if response.status_code == 429:
                retry_after = int(response.headers.get("retry-after", 1))
                time.sleep(retry_after)
                continue
            
            if response.status_code != 200:
                raise ValueError(f"Stripe API error: {response.status_code}")
            
            data = response.json()
            
            # Process subscriptions
            for sub in data.get("data", []):
                if sub.get("status") == "active":
                    customer_id = sub.get("customer_id")
                    amount = sub.get("amount", 0) / 100  # Stripe returns in cents
                    currency = sub.get("currency", "usd")
                    stripe_data[customer_id] = {
                        "mrr": amount,
                        "has_declined": False
                    }
            
            # Check for more pages
            if not data.get("has_more"):
                break
            
            page += 1
            
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            raise
        except Exception as e:
            print(f"Error fetching Stripe data: {e}")
            raise
    
    return stripe_data


def fetch_slack_data():
    """Fetch Slack channel activity with rate limit handling."""
    _, slack_token = load_env()
    base_url = "https://slack.com/api"
    
    # First get all channels
    channels_url = f"{base_url}/conversations.list"
    channels = []
    
    try:
        response = requests.post(
            channels_url,
            headers={"Authorization": f"Bearer {slack_token}"},
            data={"limit": 100}
        )
        
        if response.status_code == 429:
            time.sleep(5)
            response = requests.post(
                channels_url,
                headers={"Authorization": f"Bearer {slack_token}"},
                data={"limit": 100}
            )
        
        if response.status_code != 200:
            raise ValueError(f"Slack API error: {response.status_code}")
        
        data = response.json()
        for channel in data.get("channels", []):
            channels.append({
                "id": channel.get("id"),
                "name": channel.get("name")
            })
    except Exception as e:
        print(f"Error fetching channels: {e}")
        return {}
    
    # Fetch message history for each channel
    slack_data = {}
    for channel in channels:
        try:
            history_url = f"{base_url}/conversations.history"
            params = {
                "channel": channel["id"],
                "limit": 100,
                "inclusive": "true"
            }
            
            response = requests.post(
                history_url,
                headers={"Authorization": f"Bearer {slack_token}"},
                params=params
            )
            
            if response.status_code == 429:
                time.sleep(5)
                continue
            
            if response.status_code != 200:
                continue
            
            data = response.json()
            messages = data.get("messages", [])
            total = len(messages)
            
            # Calculate average daily activity (over 30 days)
            avg_daily = total / 30
            
            slack_data[channel["name"]] = {
                "total_messages": total,
                "avg_daily": avg_daily
            }
            
        except Exception as e:
            print(f"Error fetching channel {channel['name']}: {e}")
            continue
    
    return slack_data
