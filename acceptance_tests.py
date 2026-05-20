import unittest
import unittest.mock
import sys
sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')

from stripe_client import fetch_active_subscriptions
from mrr_calculator import calculate_mrr
import requests

class TestSaaSChurnCLI(unittest.TestCase):
    @unittest.mock.patch('requests.get')
    def test_fetch_active_subscriptions(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'data': [{'id': 'sub_1'}]}
        result = fetch_active_subscriptions('fake_key')
        self.assertEqual(result, [{'id': 'sub_1'}])

    def test_calculate_mrr(self):
        subs = [{'lines': {'data': [{'plan': {'amount': 1000}}]}}]
        self.assertEqual(calculate_mrr(subs), 10.0)

if __name__ == '__main__':
    unittest.main()