import pytest
import responses
import stripe
import os
from click.testing import CliRunner
from saaschurn.core import SaaSChurnAnalyzer
from saaschurn.cli import cli

os.environ['STRIPE_API_TOKEN'] = 'sk_test_123'
os.environ['SLACK_API_TOKEN'] = 'xoxb-123'

@responses.activate
def test_criterion_2_fetch_subscriptions():
    responses.add(
        responses.GET,
        "https://api.stripe.com/v1/subscriptions",
        json={'data': [{'plan': {'amount': 1000}}]},
        status=200
    )
    analyzer = SaaSChurnAnalyzer()
    subs = analyzer.fetch_active_subscriptions()
    assert len(subs) == 1

def test_criterion_2_calculate_mrr():
    analyzer = SaaSChurnAnalyzer()
    subs = [{'plan': {'amount': 1000}}]
    mrr = analyzer.calculate_mrr(subs)
    assert mrr == 10.0

@responses.activate
def test_criterion_3_pull_slack_activity():
    responses.add(
        responses.GET,
        "https://slack.com/api/conversations.history",
        json={'messages': [{'text': 'hello'}]},
        status=200
    )
    analyzer = SaaSChurnAnalyzer()
    activity = analyzer.pull_slack_activity(['C123456'])
    assert len(activity) == 1

def test_criterion_4_compute_churn_score():
    analyzer = SaaSChurnAnalyzer()
    score = analyzer.compute_churn_score(500, [{'messages': 2}])
    assert score == 1.0

def test_criterion_5_rich_table_output():
    runner = CliRunner()
    result = runner.invoke(cli, ['health', '--output', 'table'])
    assert result.exit_code == 0

def test_criterion_6_dry_run():
    runner = CliRunner()
    result = runner.invoke(cli, ['health', '--dry-run'])
    assert result.exit_code == 0

def test_criterion_6_json_export():
    runner = CliRunner()
    result = runner.invoke(cli, ['health', '--output', 'json'])
    assert result.exit_code == 0
