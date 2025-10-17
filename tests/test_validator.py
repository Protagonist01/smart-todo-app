"""
Unit tests for validator module.
"""

import pytest
from src.parsers.validator import (
    validate_email,
    validate_priority,
    validate_date_format,
    validate_date_not_past,
    validate_tag,
    validate_time_format,
    validate_task_data,
    sanitize_description
)


class TestValidateEmail:
    """Tests for email validation."""
    
    def test_valid_email(self):
        """Test valid email addresses."""
        assert validate_email("alice@example.com") is True
        assert validate_email("john.doe@company.co.uk") is True
        assert validate_email("user123@test.org") is True
    
    def test_invalid_email(self):
        """Test invalid email addresses."""
        assert validate_email("notanemail") is False
        assert validate_email("missing@domain") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False
    
    def test_empty_email(self):
        """Test empty email."""
        assert validate_email("") is False
        assert validate_email(None) is False


class TestValidatePriority:
    """Tests for priority validation."""
    
    def test_valid_priority(self):
        """Test valid priority levels."""
        assert validate_priority("high") is True
        assert validate_priority("medium") is True
        assert validate_priority("low") is True
        assert validate_priority("HIGH") is True  # Case insensitive
    
    def test_invalid_priority(self):
        """Test invalid priority levels."""
        assert validate_priority("critical") is False
        assert validate_priority("urgent") is False
        assert validate_priority("") is False


class TestValidateDateFormat:
    """Tests for date format validation."""
    
    def test_valid_date_format(self):
        """Test valid date formats."""
        assert validate_date_format("2025-10-20") is True
        assert validate_date_format("2025-01-01") is True
    
    def test_invalid_date_format(self):
        """Test invalid date formats."""
        assert validate_date_format("10/20/2025") is False
        assert validate_date_format("2025-13-01") is False  # Invalid month
        assert validate_date_format("2025-10-32") is False  # Invalid day
        assert validate_date_format("tomorrow") is False


class TestValidateTag:
    """Tests for tag validation."""
    
    def test_valid_tag(self):
        """Test valid tags."""
        assert validate_tag("shopping") is True
        assert validate_tag("work_2024") is True
        assert validate_tag("urgent123") is True
    
    def test_invalid_tag(self):
        """Test invalid tags."""
        assert validate_tag("@shopping") is False  # @ not allowed
        assert validate_tag("work-2024") is False  # - not allowed
        assert validate_tag("tag with spaces") is False
        assert validate_tag("") is False


class TestValidateTaskData:
    """Tests for complete task data validation."""
    
    def test_valid_task_data(self):
        """Test valid task data."""
        data = {
            'description': 'Buy milk',
            'priority': 'high',
            'tags': ['shopping', 'urgent'],
            'assigned_to': 'alice@example.com',
            'due_date': '2025-10-20'
        }
        is_valid, errors = validate_task_data(data)
        assert is_valid is True
        assert len(errors) == 0
    
    def test_missing_description(self):
        """Test missing description."""
        data = {}
        is_valid, errors = validate_task_data(data)
        assert is_valid is False
        assert any('description' in err.lower() for err in errors)
    
    def test_empty_description(self):
        """Test empty description."""
        data = {'description': '   '}
        is_valid, errors = validate_task_data(data)
        assert is_valid is False
    
    def test_invalid_priority(self):
        """Test invalid priority."""
        data = {'description': 'Task', 'priority': 'critical'}
        is_valid, errors = validate_task_data(data)
        assert is_valid is False
        assert any('priority' in err.lower() for err in errors)
    
    def test_invalid_email(self):
        """Test invalid email."""
        data = {'description': 'Task', 'assigned_to': 'not-an-email'}
        is_valid, errors = validate_task_data(data)
        assert is_valid is False
        assert any('email' in err.lower() for err in errors)


class TestSanitizeDescription:
    """Tests for description sanitization."""
    
    def test_remove_extra_whitespace(self):
        """Test removing extra whitespace."""
        assert sanitize_description("  Buy   milk  ") == "Buy milk"
        assert sanitize_description("Task\n\nwith\nnewlines") == "Task with newlines"
    
    def test_trim_whitespace(self):
        """Test trimming whitespace."""
        assert sanitize_description("  Task  ") == "Task"
    
    def test_empty_string(self):
        """Test empty string."""
        assert sanitize_description("") == ""
        assert sanitize_description("   ") == ""