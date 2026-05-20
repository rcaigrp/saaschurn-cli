import pytest
import unittest.mock as mock
import json
from click.testing import CliRunner
from saaschurn.cli import cli
from saaschurn.churn import compute_churn_score
from saaschurn.output import format_table

class TestAcceptanceCriteria:
    @mock.patch.dict('os.environ', {'STRIPE_API_TOKEN': 'sk_test_abc', 'SLACK_API_TOKEN': 'xoxb_abc'})
    def test_criterion_1_auth_via_env(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['--dry-run'])
        assert result.exit_code == 0
        assert 'Churn Score' in result.output

    @mock.patch('stripe.Subscription.list')
    def test_criterion_2_fetch_subscriptions(self, mock_list):
        mock_list.return_value = {'data': [{'status': 'active', 'amount': 100}]}
        from saaschurn.churn import fetch_subscriptions
        data = fetch_subscriptions()
        assert isinstance(data, list)
        assert len(data) > 0

    @mock.patch('slack_sdk.web.SlackClient.conversations_history')
    def test_criterion_3_pull_slack_logs(self, mock_history):
        mock_history.return_value = {'messages': [{'text': 'hello'}]}
        from saaschurn.churn import pull_slack_logs
        data = pull_slack_logs()
        assert isinstance(data, list)

    def test_criterion_4_compute_churn_score(self):
        score = compute_churn_score(0.2, 0.3)
        assert 0 <= score <= 1

    def test_criterion_5_rich_table_output(self):
        data = [{'client': 'TestCo', 'score': 0.5}]
        table = format_table(data)
        assert 'TestCo' in table

    def test_criterion_6_dry_run_and_json(self):
        runner = CliRunner()
        result_dry = runner.invoke(cli, ['--dry-run'])
        assert result_dry.exit_code == 0
        result_json = runner.invoke(cli, ['--output', 'json'])
        assert result_json.exit_code == 0
        assert result_json.output.startswith('{')
