import unittest
import responses
import sys
import os
import json

sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')

from saaschurn.stripe_client import fetch_active_subscriptions, calc_mrr

class TestStripeClient(unittest.TestCase):
    @responses.activate
    def test_fetch_active_subscriptions(self):
        mock_data = {
            "object": "list",
            "data": [
                {"plan": {"amount": 1000, "currency": "usd"}, "status": "active"},
                {"plan": {"amount": 2000, "currency": "usd"}, "status": "active"}
            ]
        }
        responses.add(
            responses.GET,
            "https://api.stripe.com/v1/subscriptions",
            json=mock_data,
            status=200
        )
        
        token = "fake_token"
        result = fetch_active_subscriptions(token)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["plan"]["amount"], 1000)

    @responses.activate
    def test_calc_mrr(self):
        subscriptions = [
            {"plan": {"amount": 1000, "currency": "usd"}},
            {"plan": {"amount": 2000, "currency": "usd"}}
        ]
        mrr = calc_mrr(subscriptions)
        self.assertEqual(mrr, 30.0)

    @responses.activate
    def test_fetch_active_subscriptions_error(self):
        responses.add(
            responses.GET,
            "https://api.stripe.com/v1/subscriptions",
            status=401,
            body="Unauthorized"
        )
        token = "bad_token"
        result = fetch_active_subscriptions(token)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
