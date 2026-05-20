import pytest
import os
import sys
import json
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_criterion_1_auth_env_vars():
    """Test that CLI checks env vars."""
    with patch.dict(os.environ, {}, clear=True):
        with patch('cli.console') as mock_console:
            from cli import main
            main()
            assert mock_console.print.called
            calls = [str(c.args) for c in mock_console.print.call_args_list]
            assert any('Missing env vars' in c for c in calls)

def test_criterion_2_fetch_subscriptions():
    """Test fetching subscriptions and calculating MRR."""
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test', 'SLACK_API_TOKEN': 'xoxb_test'}):
        with patch('cli.stripe') as mock_stripe:
            mock_sub = MagicMock(status='active', plan=MagicMock(amount=1000))
            mock_stripe.Subscription.list.return_value = MagicMock(data=[mock_sub])
            
            from cli import fetch_subscriptions, calculate_mrr
            
            subs = fetch_subscriptions('sk_test')
            assert len(subs) == 1
            assert subs[0].status == 'active'
            
            mrr = calculate_mrr(subs)
            assert abs(mrr - 10.0) < 0.01

def test_criterion_3_pull_slack_activity():
    """Test fetching slack activity."""
    with patch('cli.requests') as mock_requests:
        mock_resp = MagicMock(status_code=200)
        mock_requests.get.return_value = mock_resp
        
        from cli import fetch_slack_activity
        channels = fetch_slack_activity('xoxb_test', ['c1'])
        assert len(channels) == 1

def test_criterion_4_dry_run():
    """Test dry-run mode."""
    with patch('cli.console') as mock_console:
        from cli import main
        import argparse
        
        def mock_parse_args(*args, **kwargs):
            class Args:
                dry_run = True
                output = 'console'
            return Args()
        
        with patch('argparse.ArgumentParser.parse_args', mock_parse_args):
            main()
            assert any('Dry-run' in str(call.args) for call in mock_console.print.call_args_list)

def test_criterion_5_json_output():
    """Test JSON output mode."""
    with patch.dict(os.environ, {'STRIPE_API_TOKEN': 'sk_test', 'SLACK_API_TOKEN': 'xoxb_test'}):
        with patch('cli.stripe') as mock_stripe:
            with patch('cli.requests') as mock_requests:
                mock_sub = MagicMock(status='active', plan=MagicMock(amount=1000))
                mock_stripe.Subscription.list.return_value = MagicMock(data=[mock_sub])
                
                from cli import main
                import argparse
                
                def mock_parse_args(*args, **kwargs):
                    class Args:
                        dry_run = False
                        output = 'json'
                    return Args()
                
                with patch('argparse.ArgumentParser.parse_args', mock_parse_args):
                    with patch('cli.console') as mock_console:
                        main()
                        calls = [str(c.args) for c in mock_console.print.call_args_list]
                        assert any('json' in c.lower() or 'mrr' in c.lower() for c in calls)
