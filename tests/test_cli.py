"""
Basic tests for CLI interface.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.interface import TodoCLI


@pytest.fixture
def cli():
    """Create CLI instance for testing."""
    with patch('src.cli.interface.TaskService'):
        cli = TodoCLI()
        cli.service = MagicMock()
        return cli


class TestCLI:
    """CLI tests."""
    
    def test_initialization(self, cli):
        """Test CLI initializes correctly."""
        assert cli.running is True
        assert cli.service is not None
    
    def test_cmd_add(self, cli):
        """Test add command."""
        cli.service.add_task_from_string.return_value = "task-123"
        cli.service.get_task.return_value = MagicMock(
            description="Buy milk",
            tags=["shopping"],
            priority="high",
            is_complete=False,
            id="task-123",
            due_date=None,
            time=None,
            assigned_to=None
        )
        
        cli.cmd_add(["Buy", "milk", "@shopping", "#high"])
        
        cli.service.add_task_from_string.assert_called_once()
    
    def test_cmd_list(self, cli):
        """Test list command."""
        cli.service.list_all.return_value = []
        
        cli.cmd_list([])
        
        cli.service.list_all.assert_called_once()
    
    def test_cmd_complete(self, cli):
        """Test complete command."""
        cli.service.mark_complete.return_value = True
        
        with patch.object(cli, '_find_task_id', return_value='task-123'):
            cli.cmd_complete(['task-123'])
        
        cli.service.mark_complete.assert_called_once()
    
    def test_process_command(self, cli):
        """Test command processing."""
        with patch.object(cli, 'cmd_add') as mock_add:
            cli.process_command("add Buy milk")
            mock_add.assert_called_once()
    
    def test_exit_command(self, cli):
        """Test exit command."""
        assert cli.running is True
        
        cli.exit_app()
        
        assert cli.running is False