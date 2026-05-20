import unittest
from unittest.mock import patch
from saaschurn.churn import calculate_churn_score

class TestChurn(unittest.TestCase):
    def test_churn_score_high(self):
        score = calculate_churn_score({"decline_percent": 15}, {"activity_drop_percent": 25})
        self.assertEqual(score, 100)

    def test_churn_score_low(self):
        score = calculate_churn_score({"decline_percent": 5}, {"activity_drop_percent": 10})
        self.assertEqual(score, 0)
