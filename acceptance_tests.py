import pytest
import responses
import json
import sys
from io import StringIO
from unittest.mock import patch, MagicMock

sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')

from saaschurn.cli import main
from saaschurn.fetchers import StripeFetcher, SlackFetcher
from saaschurn.calculators import ChurnCalculator
from saaschurn.reporter import Reporter

# Mock Data
MOCK_STRIPE_SUBS = [
    {'id': 'sub_1', 'customer_id': 'cus_1', 'plan_id': 'plan_1', 'status': 'active', 'amount': 1000, 'currency': 'usd'},
    {'id': 'sub_2', 'customer_id': 'cus_1', 'plan_id': 'plan_2', 'status': 'active', 'amount': 500, 'currency': 'usd'},
]

MOCK_SLACK_MSGS = [
    {'text': 'Hello', 'ts': '123'},
    {'text': 'World', 'ts': '456'},
]

MOCK_ENV = {'STRIPE_API_KEY': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}

class TestAcceptanceCriteria:
    @responses.activate
    def test_criterion_2_fetch_subscriptions(self):
        responses.add(responses.GET, 'https://api.stripe.com/v1/subscriptions', json=MOCK_STRIPE_SUBS)
        fetcher = StripeFetcher()
        subs = fetcher.fetch()
        assert len(subs) == 2

    @responses.activate
    def test_criterion_3_pull_slack_activity(self):
        responses.add(responses.GET, 'https://slack.com/api/conversations.history', json=MOCK_SLACK_MSGS)
        fetcher = SlackFetcher()
        activity = fetcher.fetch('ch_1')
        assert len(activity) == 2

    def test_criterion_4_compute_churn_score(self):
        calc = ChurnCalculator()
        score = calc.calculate(mrr=1000, activity=5)
        assert 0 <= score <= 100

    def test_criterion_5_output_rich_table(self):
        with patch('sys.stdout', new_callable=lambda: StringIO()) as fake_out:
            Reporter().print_report([('Client A', 1500, 5, 'MEDIUM', 'Review')])
            output = fake_out.getvalue()
            assert 'Client A' in output

    def test_criterion_6_dry_run_and_json(self):
        with patch('sys.stdout', new_callable=lambda: StringIO()) as fake_out:
            with patch.dict('os.environ', MOCK_ENV):
                main(['health', '--dry-run'])
                output = fake_out.getvalue()
                assert 'DUMMY' in output

        with patch('sys.stdout', new_callable=lambda: StringIO()) as fake_out:
            with patch.dict('os.environ', MOCK_ENV):
                main(['health', '--output', 'json'])
                output = fake_out.getvalue()
                assert 'DUMMY' in output
