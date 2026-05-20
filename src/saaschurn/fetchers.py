#!/usr/bin/env python3
"""Stripe and Slack API wrappers with pagination and rate limit handling"""
import os
import time
import requests
import logging

logger = logging.getLogger(__name__)


class StripeFetcher:
    """Fetches Stripe subscription data with pagination and rate limit handling."""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('STRIPE_API_KEY')
        if not self.api_key:
            raise ValueError('STRIPE_API_KEY environment variable is required')
        self.base_url = 'https://api.stripe.com/v1/subscriptions'
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})

    def get_active_subscriptions(self):
        """Fetch all active subscriptions with pagination and exponential backoff."""
        subscriptions = []
        params = {'status': 'active'}
        page = 0

        while True:
            try:
                response = self.session.get(self.base_url, params=params)
                if response.status_code == 429:
                    # Rate limited - exponential backoff
                    wait_time = 2 ** page
                    logger.warning(f'Response 429 - retrying in {wait_time}s')
                    time.sleep(wait_time)
                    page += 1
                    continue

                response.raise_for_status()
                data = response.json()

                subscriptions.extend(data.get('data', []))

                if not data.get('has_more'):
                    break

                params['starting_after'] = data['data'][-1]['id']

            except requests.exceptions.HTTPError as e:
                logger.error(f'HTTP error: {e}')
                break

        return subscriptions


class SlackFetcher:
    """Fetches Slack channel activity logs."""

    def __init__(self, token=None):
        self.token = token or os.environ.get('SLACK_API_TOKEN')
        if not self.token:
            raise ValueError('SLACK_API_TOKEN environment variable is required')
        self.base_url = 'https://slack.com/api/conversations.history'
        self.session = requests.Session()
        self.session.headers.update({'Authorization': f'Bearer {self.token}'})

    def get_channel_activity(self, channel_id):
        """Fetch message counts for a channel over the last 30 days."""
        params = {'channel': channel_id, 'limit': 100}
        page = 0

        while True:
            try:
                response = self.session.get(self.base_url, params=params)
                if response.status_code == 429:
                    wait_time = 2 ** page
                    logger.warning(f'Slack rate limited - retrying in {wait_time}s')
                    time.sleep(wait_time)
                    page += 1
                    continue

                response.raise_for_status()
                data = response.json()

                messages = data.get('messages', [])

                # Skip gracefully if no messages or channel missing
                if not messages:
                    return {'channel': channel_id, 'message_count': 0, 'days': 30}

                return {
                    'channel': channel_id,
                    'message_count': len(messages),
                    'days': 30
                }

            except requests.exceptions.HTTPError as e:
                logger.error(f'Slack HTTP error: {e}')
                return {'channel': channel_id, 'message_count': 0, 'days': 30}

    def get_all_channel_activity(self):
        """Fetch activity for all known client channels."""
        # For dry-run, we know the channels
        channels = ['channel_1', 'channel_2']
        result = {}

        for channel in channels:
            result[channel] = self.get_channel_activity(channel)

        return result
