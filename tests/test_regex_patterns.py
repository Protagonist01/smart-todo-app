"""
Unit tests for regex patterns.
"""

import pytest
import re
from src.parsers.regex_patterns import (
    TAG_PATTERN,
    PRIORITY_PATTERN,
    DUE_DATE_PATTERN,
    EMAIL_PATTERN,
    TIME_PATTERN,
    COMPILED_TAG,
    COMPILED_PRIORITY,
    COMPILED_DUE_DATE,
    COMPILED_EMAIL,
    get_pattern
)


class TestTagPattern:
    """Tests for tag extraction pattern."""
    
    def test_single_tag(self):
        """Test extracting a single tag."""
        text = "Buy groceries @shopping"
        matches = re.findall(TAG_PATTERN, text)
        assert matches == ['shopping']
    
    def test_multiple_tags(self):
        """Test extracting multiple tags."""
        text = "Complete project @work @urgent @coding"
        matches = re.findall(TAG_PATTERN, text)
        assert matches == ['work', 'urgent', 'coding']
    
    def test_no_tags(self):
        """Test text with no tags."""
        text = "Just a regular task"
        matches = re.findall(TAG_PATTERN, text)
        assert matches == []
    
    def test_tag_with_numbers(self):
        """Test tags containing numbers."""
        text = "Project @phase2 @q4"
        matches = re.findall(TAG_PATTERN, text)
        assert matches == ['phase2', 'q4']


class TestPriorityPattern:
    """Tests for priority extraction pattern."""
    
    def test_high_priority(self):
        """Test extracting high priority."""
        text = "Urgent task #high"
        match = re.search(PRIORITY_PATTERN, text)
        assert match.group(1) == 'high'
    
    def test_medium_priority(self):
        """Test extracting medium priority."""
        text = "Regular task #medium"
        match = re.search(PRIORITY_PATTERN, text)
        assert match.group(1) == 'medium'
    
    def test_low_priority(self):
        """Test extracting low priority."""
        text = "Minor task #low"
        match = re.search(PRIORITY_PATTERN, text)
        assert match.group(1) == 'low'
    
    def test_case_insensitive(self):
        """Test priority pattern is case insensitive."""
        text = "Task #HIGH"
        match = re.search(PRIORITY_PATTERN, text, re.IGNORECASE)
        assert match is not None
    
    def test_invalid_priority(self):
        """Test invalid priority levels are not matched."""
        text = "Task #critical"
        match = re.search(PRIORITY_PATTERN, text)
        assert match is None


class TestDueDatePattern:
    """Tests for due date extraction pattern."""
    
    def test_valid_date(self):
        """Test extracting valid date."""
        text = "Submit report due:2025-10-20"
        match = re.search(DUE_DATE_PATTERN, text)
        assert match.group(1) == '2025-10-20'
    
    def test_date_format(self):
        """Test date format YYYY-MM-DD."""
        text = "Task due:2025-12-31"
        match = re.search(DUE_DATE_PATTERN, text)
        assert match is not None
    
    def test_invalid_date_format(self):
        """Test invalid date formats are not matched."""
        text = "Task due:10/20/2025"
        match = re.search(DUE_DATE_PATTERN, text)
        assert match is None


class TestEmailPattern:
    """Tests for email extraction pattern."""
    
    def test_valid_email(self):
        """Test extracting valid email."""
        text = "Task assigned:alice@example.com"
        match = re.search(EMAIL_PATTERN, text)
        assert match.group(1) == 'alice@example.com'
    
    def test_email_with_dots(self):
        """Test email with dots in username."""
        text = "assigned:john.doe@company.co.uk"
        match = re.search(EMAIL_PATTERN, text)
        assert match.group(1) == 'john.doe@company.co.uk'
    
    def test_email_with_numbers(self):
        """Test email with numbers."""
        text = "assigned:user123@test.org"
        match = re.search(EMAIL_PATTERN, text)
        assert match.group(1) == 'user123@test.org'
    
    def test_invalid_email(self):
        """Test invalid email is not matched."""
        text = "assigned:notanemail"
        match = re.search(EMAIL_PATTERN, text)
        assert match is None


class TestTimePattern:
    """Tests for time extraction pattern."""
    
    def test_time_with_am(self):
        """Test time with AM."""
        text = "Meeting at 9am"
        match = re.search(TIME_PATTERN, text)
        assert match is not None
        assert match.group(1) == '9'
    
    def test_time_with_minutes(self):
        """Test time with minutes."""
        text = "Call by 3:30pm"
        match = re.search(TIME_PATTERN, text)
        assert match.group(1) == '3'
        assert match.group(2) == '30'
    
    def test_24_hour_format(self):
        """Test 24-hour format."""
        text = "Deadline at 14:00"
        match = re.search(TIME_PATTERN, text)
        assert match.group(1) == '14'
        assert match.group(2) == '00'


class TestGetPattern:
    """Tests for get_pattern helper function."""
    
    def test_get_tag_pattern(self):
        """Test retrieving tag pattern."""
        pattern = get_pattern('tag')
        assert pattern is not None
        assert pattern == COMPILED_TAG
    
    def test_get_priority_pattern(self):
        """Test retrieving priority pattern."""
        pattern = get_pattern('priority')
        assert pattern is not None
        assert pattern == COMPILED_PRIORITY
    
    def test_get_nonexistent_pattern(self):
        """Test retrieving non-existent pattern returns None."""
        pattern = get_pattern('nonexistent')
        assert pattern is None


class TestIntegration:
    """Integration tests with realistic task strings."""
    
    def test_complete_task_string(self):
        """Test parsing a complete task string with all components."""
        text = "Buy groceries @shopping #high due:2025-10-20 assigned:alice@example.com at 3pm"
        
        tags = re.findall(TAG_PATTERN, text)
        priority = re.search(PRIORITY_PATTERN, text)
        due_date = re.search(DUE_DATE_PATTERN, text)
        email = re.search(EMAIL_PATTERN, text)
        time = re.search(TIME_PATTERN, text)
        
        assert tags == ['shopping']
        assert priority.group(1) == 'high'
        assert due_date.group(1) == '2025-10-20'
        assert email.group(1) == 'alice@example.com'
        assert time.group(1) == '3'