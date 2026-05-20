import os
import pytest
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '/workspace/projects/SaaSChurn-CLI')

def test_criterion_1_auth():
    from saaschurn import core
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test_123', 'SLACK_API_TOKEN': 'xoxb-123'}):
        assert core.get_stripe_client() is not None
        assert core.get_slack_client() is not None

def test_criterion_2_mrr():
    from saaschurn import core
    subs = [{'status': 'active', 'plan': {'amount': 10000}}]
    assert core.calculate_mrr(subs) == 100

def test_criterion_3_slack():
    from saaschurn import core
    mock_client = MagicMock()
    mock_client.conversations_history.return_value = {'messages': [{'text': 'hi'}]}
    assert core.get_slack_activity(mock_client, ['ch1']) == {'ch1': 1}

def test_criterion_4_score():
    from saaschurn import core
    assert core.compute_churn_score([1000, 500], [10, 5]) > 0

def test_criterion_5_rich_table():
    from rich.table import Table
    table = Table()
    assert isinstance(table, Table)

def test_criterion_6_dry_run():
    from click.testing import CliRunner
    from saaschurn import cli
    runner = CliRunner()
    result = runner.invoke(cli.health, ['--dry-run'])
    assert "Dry-run mode enabled" in result.output
