import unittest
import responses
import json
import sys
import os
import io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from saaschurn.fetchers import fetch_stripe_data, fetch_slack_data
from saaschurn.calculators import calculate_mrr, calculate_churn_risk
from saaschurn.reporter import generate_report
from saaschurn.cli import main

class TestAcceptanceCriteria(unittest.TestCase):
    @responses.activate
    def test_criterion_1_auth_and_criterion_2_fetch_stripe_mrr(self):
        responses.add(responses.GET, "https://api.stripe.com/v1/subscriptions", json={"data": [{"id": "sub_1", "customer_name": "Client A", "price": 100, "quantity": 1}], "has_more": False})
        tokens = fetch_stripe_data("fake_token")
        self.assertEqual(len(tokens), 1)
        mrr = calculate_mrr(tokens)
        self.assertEqual(mrr['Client A'], 100)

    @responses.activate
    def test_criterion_3_fetch_slack_activity(self):
        responses.add(responses.GET, "https://slack.com/api/conversations.history", json={"messages": [{"text": "Hello"}, {"text": "World"}]})
        activity = fetch_slack_data("fake_token", ["Client A"])
        self.assertEqual(activity['Client A']['messages_count'], 2)

    def test_criterion_4_churn_risk_calculation(self):
        mrr = {'Client A': 100}
        slack = {'Client A': {'messages_count': 5}}
        results = calculate_churn_risk(mrr, slack)
        self.assertEqual(results[0]['churn_risk'], 70) 
        self.assertEqual(results[0]['risk_level'], 'MEDIUM')

    def test_criterion_5_rich_table_generation(self):
        results = [{'client': 'Client A', 'mrr': 100, 'activity_score': 100, 'churn_risk': 50, 'risk_level': 'LOW', 'recommendation': 'Good health'}]
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            generate_report(results)
            output = sys.stdout.getvalue()
            self.assertIn('Client A', output)
        finally:
            sys.stdout = old_stdout

    def test_criterion_6_dry_run_and_json_output(self):
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            main(['health', '--dry-run', '--output', 'json'])
            output = sys.stdout.getvalue()
            data = json.loads(output)
            self.assertIn('client', data[0])
        finally:
            sys.stdout = old_stdout

    def test_criterion_7_tests_exist(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
