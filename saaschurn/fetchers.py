import os
import requests
import time


class StripeFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('STRIPE_API_KEY')
        self.base_url = 'https://api.stripe.com/v1/subscriptions'

    def fetch(self):
        headers = {'Authorization': f'Bearer {self.api_key}'}
        params = {'limit': 100}
        all_subs = []
        url = self.base_url

        while True:
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()

                if isinstance(data, dict):
                    items = data.get('data', [])
                    url = data.get('next_url')
                else:
                    items = data
                    url = None

                all_subs.extend(items)

                if not url:
                    break

                # Rate limit handling
                time.sleep(0.5)

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    wait_time = 2 ** e.response.status_code
                    print(f'Rate limited. Waiting {wait_time} seconds...')
                    time.sleep(wait_time)
                    continue
                raise

        return all_subs

    def fetch_mock(self):
        return [
            {'id': 'sub_001', 'customer_name': 'Acme Corp', 'status': 'active',
             'current_period_amount': 100000, 'previous_period_amount': 120000},
            {'id': 'sub_002', 'customer_name': 'Globex Inc', 'status': 'active',
             'current_period_amount': 200000, 'previous_period_amount': 190000},
            {'id': 'sub_003', 'customer_name': 'Initech', 'status': 'active',
             'current_period_amount': 50000, 'previous_period_amount': 60000}
        ]


class SlackFetcher:
    def __init__(self, token=None):
        self.token = token or os.getenv('SLACK_API_TOKEN')
        self.url = 'https://slack.com/api/conversations.history'
        self.channels = {
            'Acme Corp': 'C12345',
            'Globex Inc': 'C67890',
            'Initech': 'C11111'
        }

    def fetch(self):
        headers = {'Authorization': f'Bearer {self.token}'}
        activity = {}

        for client, channel_id in self.channels.items():
            params = {'channel': channel_id, 'limit': 100}
            try:
                response = requests.get(self.url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                messages = data.get('messages', [])
                activity[client] = {'channel_id': channel_id, 'message_count': len(messages)}
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    time.sleep(2 ** e.response.status_code)
                    continue
                activity[client] = {'channel_id': channel_id, 'message_count': 0}

        return activity

    def fetch_mock(self):
        return {
            'Acme Corp': {'channel_id': 'C12345', 'message_count': 5},
            'Globex Inc': {'channel_id': 'C67890', 'message_count': 150},
            'Initech': {'channel_id': 'C11111', 'message_count': 8}
        }
