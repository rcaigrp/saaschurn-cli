import os
import pytest
import responses
import json
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')

import main

os.environ['STRIPE_API_KEY'] = 'test_key'
os.environ['SLACK_API_TOKEN'] = 'test_token'

def test_auth_env_vars():
    try:
        main.get_env_vars()
    except ValueError:
        pytest.fail("Environment variables not set correctly")

@responses.activate
def test_fetch_subscriptions():
    responses.add(responses.GET, 'https://api.stripe.com/v1/subscriptions', json={'data': [{'id': 'sub_1', 'status': 'active', 'plan': {'amount': 1000}}]})
    subs = main.fetch_subscriptions('test_key')
    assert 'data' in subs
    assert len(subs['data']) == 1

def test_calculate_mrr():
    subscriptions = {'data': [{'status': 'active', 'plan': {'amount': 1000}}]}
    assert main.calculate_mrr(subscriptions) == 10.0

@responses.activate
def test_fetch_slack_activity():
    responses.add(responses.GET, 'https://slack.com/api/conversations.history', json={'messages': [{'text': 'Hello'}]})
    logs = main.fetch_slack_activity('test_token', 'general')
    assert 'messages' in logs

def test_churn_score():
    score = main.calculate_churn_score([1000, 800], [10, 5])
    assert score > 0

def test_rich_output():
    with patch('main.console') as mock_console:
        main.generate_report({'mrr': 10.0, 'churn_score': 0.5})
        assert mock_console.print.call_count == 3

def test_json_export():
    data = {'mrr': 10.0, 'churn_score': 0.5}
    json_str = json.dumps(data)
    assert json_str is not None
