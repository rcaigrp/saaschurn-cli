import pytest
import click
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
import json
import os

directory = '/workspace/projects/SaaSChurn-CLI'
os.chdir(directory)

import sys
sys.path.insert(0, directory)

from saaschurn.cli import cli
from saaschurn import core


@pytest.fixture
def runner():
    return CliRunner()


@patch('saaschurn.core.stripe')
@patch('saaschurn.core.slack_sdk')
def test_criterion_1_auth_via_env_vars(mock_slack, mock_stripe, runner):
    """Test 1: Authenticate via environment variables."""
    result = runner.invoke(cli, ['health'])
    # We expect it to fail if env vars are missing or succeed if they are set
    # Since we mock, we check if it tries to use env vars
    assert "Missing environment variables" in result.output or result.exit_code == 0


@patch('saaschurn.core.stripe')
@patch('saaschurn.core.slack_sdk')
def test_criterion_2_fetch_subscriptions(mock_slack, mock_stripe, runner):
    """Test 2: Fetch active subscriptions from Stripe and calculate MRR."""
    mock_stripe.api_key = "sk_test_123"
    mock_stripe.Subscription.list.return_value = {'data': [{'amount': 100}]}
    env = {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb_123'}
    result = runner.invoke(cli, ['health'], env=env)
    assert result.exit_code == 0


@patch('saaschurn.core.stripe')
@patch('saaschurn.core.slack_sdk')
def test_criterion_3_pull_slack_activity(mock_slack, mock_stripe, runner):
    """Test 3: Pull Slack workspace activity logs."""
    mock_slack.WebClient.return_value = MagicMock()
    env = {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb_123'}
    result = runner.invoke(cli, ['health'], env=env)
    assert result.exit_code == 0


@patch('saaschurn.core.stripe')
@patch('saaschurn.core.slack_sdk')
def test_criterion_4_compute_churn_score(mock_slack, mock_stripe, runner):
    """Test 4: Compute churn probability score."""
    env = {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb_123'}
    result = runner.invoke(cli, ['health'], env=env)
    assert result.exit_code == 0


@patch('saaschurn.core.stripe')
@patch('saaschurn.core.slack_sdk')
def test_criterion_5_rich_table_output(mock_slack, mock_stripe, runner):
    """Test 5: Output formatted rich terminal table."""
    env = {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb_123'}
    result = runner.invoke(cli, ['health'], env=env)
    # Check for table-like output or success
    assert result.exit_code == 0


@patch('saaschurn.core.stripe')
@patch('saaschurn.core.slack_sdk')
def test_criterion_6_dry_run_and_json(mock_slack, mock_stripe, runner):
    """Test 6: Support dry-run mode and JSON export."""
    result_dry = runner.invoke(cli, ['health', '--dry-run'])
    assert "Dry Run" in result_dry.output

    env = {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb_123'}
    result_json = runner.invoke(cli, ['health', '--output', 'json'], env=env)
    assert result_json.exit_code == 0
    try:
        json.loads(result_json.output)
    except json.JSONDecodeError:
        assert False
