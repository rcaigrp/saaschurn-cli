import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_stripe():
    with patch('stripe.Subscription') as mock_sub:
        mock_sub.list.return_value.data = []
        yield mock_sub

@pytest.fixture
def mock_slack():
    with patch('slack_sdk.WebClient') as mock_client:
        mock_client.return_value = MagicMock()
        mock_client.return_value.conversations = MagicMock()
        mock_client.return_value.conversations.list.return_value = {'channels': []}
        mock_client.return_value.conversations.history.return_value = {'messages': []}
        yield mock_client
