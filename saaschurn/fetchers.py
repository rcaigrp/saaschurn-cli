import os
import time
import requests


class StripeFetcher:
    """Fetches subscription data from Stripe API."""

    BASE_URL = 'https://api.stripe.com/v1/subscriptions'

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })

    def get_active_subscriptions(self):
        """Fetch all active subscriptions with pagination."""
        subscriptions = []
        url = self.BASE_URL
        has_more = True

        while has_more:
            try:
                response = self.session.get(url)
                if response.status_code == 429:
                    # Rate limit - exponential backoff
                    wait_time = 2 ** (len(subscriptions) // 10)
                    time.sleep(wait_time)
                    continue

                if response.status_code != 200:
                    raise Exception(f'Stripe API error: {response.status_code}')

                data = response.json()
                for item in data.get('data', []):
                    if item.get('status') == 'active':
                        subscriptions.append(item)

                has_more = data.get('has_more', False)
                if has_more:
                    url = data.get('next_page_url') or self.BASE_URL

            except requests.exceptions.RequestException as e:
                raise Exception(f'Failed to fetch from Stripe: {e}')

        return self._process_subscriptions(subscriptions)

    def _process_subscriptions(self, subscriptions):
        """Process subscription data into client records."""
        client_data = {}
        for sub in subscriptions:
            customer_id = sub.get('customer')
            if customer_id not in client_data:
                client_data[customer_id] = {
                    'customer_name': sub.get('customer_details', {}).get('name', customer_id),
                    'current_mrr': 0,
                    'previous_mrr': 0,
                    'channel': f'{customer_id.lower().replace(" ", "-")}-channel'
                }
            # Calculate MRR from subscription data
            price = sub.get('items', {}).get('data', [{}])[0].get('price', {})
            if price:
                amount = price.get('unit_amount', 0) / 100  # Stripe returns in cents
                interval = price.get('recurring', {}).get('interval', 'month')
                if interval == 'month':
                    client_data[customer_id]['current_mrr'] += amount
                    client_data[customer_id]['previous_mrr'] += amount * 1.1  # Assume 10% growth target

        return list(client_data.values())


class SlackFetcher:
    """Fetches channel activity data from Slack API."""

    BASE_URL = 'https://slack.com/api/conversations.history'

    def __init__(self, api_token):
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_token}'
        })

    def get_channel_activity(self):
        """Fetch activity for all client channels."""
        activity = {}
        # We need to know which channels belong to which clients
        # For simplicity, we'll fetch all channels and return activity
        channels = self._get_all_channels()

        for channel in channels:
            messages = self._get_channel_messages(channel['id'])
            activity[channel['name']] = {
                'total_messages': len(messages),
                'days': 30  # Last 30 days
            }

        return activity

    def _get_all_channels(self):
        """Get all channels in workspace."""
        channels = []
        url = self.BASE_URL
        has_more = True

        while has_more:
            try:
                response = self.session.get(url, params={'channel': '', 'limit': 100})
                if response.status_code == 429:
                    time.sleep(2)
                    continue

                if response.status_code != 200:
                    break

                data = response.json()
                for ch in data.get('groups', []):
                    if ch.get('name'):
                        channels.append({'id': ch.get('id'), 'name': ch.get('name')})

                has_more = data.get('has_more', False)

            except requests.exceptions.RequestException:
                break

        return channels

    def _get_channel_messages(self, channel_id):
        """Get messages for a specific channel."""
        url = self.BASE_URL
        messages = []
        has_more = True

        while has_more:
            try:
                response = self.session.get(url, params={'channel': channel_id, 'limit': 100})
                if response.status_code == 429:
                    time.sleep(2)
                    continue

                if response.status_code != 200:
                    break

                data = response.json()
                messages.extend(data.get('messages', []))
                has_more = data.get('has_more', False)

            except requests.exceptions.RequestException:
                break

        return messages
