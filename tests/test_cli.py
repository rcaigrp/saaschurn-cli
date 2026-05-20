import sys
import unittest
from unittest.mock import patch, MagicMock
import io


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.patcher = patch('rich.console.Console')
        self.mock_console = self.patcher.start()
        self.mock_console.return_value.print = lambda *args: None
        
    def tearDown(self):
        self.patcher.stop()
        
    @patch.dict('os.environ', {'STRIPE_API_TOKEN': 'sk_test', 'SLACK_API_TOKEN': 'xoxo'})
    @patch('sys.argv', ['main.py', 'health', '--dry-run'])
    def test_dry_run(self):
        from main import main
        main()
        calls = self.mock_console.return_value.print.call_args_list
        assert any('Dry-run mode' in str(c) for c in calls)
        
    @patch.dict('os.environ', {'STRIPE_API_TOKEN': 'sk_test', 'SLACK_API_TOKEN': 'xoxo'})
    @patch('sys.argv', ['main.py', 'health', '--output', 'json'])
    def test_json_output(self):
        from main import main
        with patch('builtins.print', return_value=None):
            main()
        
    @patch.dict('os.environ', {})
    @patch('sys.argv', ['main.py', 'health'])
    def test_missing_env_vars(self):
        from main import main
        with self.assertRaises(SystemExit):
            main()
