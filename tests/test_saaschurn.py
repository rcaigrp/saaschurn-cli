import pytest
import responses
import json
import os
import sys
import io
from unittest.mock import patch

from saaschurn.cli import main

@responses.activate
def test_criterion_1_auth_env_vars():
    with patch.dict(os.environ, {}, clear=True):
        stdout = io.StringIO()
        with patch('sys.stdout', stdout):
            with patch('sys.argv', ['cli.py']):
                try:
                    main()
                except SystemExit:
                    pass
        assert "Error: Missing STRIPE_API_TOKEN" in stdout.getvalue()

@responses.activate
def test_criterion_2_fetch_subscriptions():
    responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={"data": [{"current_period_amount": 100000}]}, status=200)
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
        stdout = io.StringIO()
        with patch('sys.stdout', stdout):
            with patch('sys.argv', ['cli.py']):
                main()
        assert "$1000.00" in stdout.getvalue()

@responses.activate
def test_criterion_3_pull_slack_activity():
    responses.add(responses.GET, "https://slack.com/api/conversations.history", json={"messages": [{"text": "hello"}]}, status=200)
    responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={"data": []}, status=200)
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
        stdout = io.StringIO()
        with patch('sys.stdout', stdout):
            with patch('sys.argv', ['cli.py']):
                main()
        assert "Churn Score" in stdout.getvalue()

@responses.activate
def test_criterion_4_compute_churn_score():
    responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={"data": [{"current_period_amount": 100}]}, status=200)
    responses.add(responses.GET, "https://slack.com/api/conversations.history", json={"messages": []}, status=200)
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
        stdout = io.StringIO()
        with patch('sys.stdout', stdout):
            with patch('sys.argv', ['cli.py']):
                main()
        assert "High Risk" in stdout.getvalue()

@responses.activate
def test_criterion_5_rich_table_output():
    responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={"data": []}, status=200)
    responses.add(responses.GET, "https://slack.com/api/conversations.history", json={"messages": []}, status=200)
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
        stdout = io.StringIO()
        with patch('sys.stdout', stdout):
            with patch('sys.argv', ['cli.py']):
                main()
        assert "MRR" in stdout.getvalue() or "Churn Score" in stdout.getvalue()

@responses.activate
def test_criterion_6_dry_run_and_json_export():
    stdout_dry = io.StringIO()
    with patch('sys.stdout', stdout_dry):
        with patch('sys.argv', ['cli.py', '--dry-run']):
            main()
    assert "Dry-run mode" in stdout_dry.getvalue()

    responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={"data": []}, status=200)
    responses.add(responses.GET, "https://slack.com/api/conversations.history", json={"messages": []}, status=200)
    stdout_json = io.StringIO()
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
        with patch('sys.stdout', stdout_json):
            with patch('sys.argv', ['cli.py', '--output', 'json']):
                main()
    assert json.loads(stdout_json.getvalue())
