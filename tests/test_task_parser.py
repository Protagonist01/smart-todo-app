"""
Unit tests for task parser module.
"""

import pytest
from src.parsers.task_parser import (
    extract_tags,
    extract_priority,
    extract_due_date,
    extract_email,
    extract_time,
    extract_duration,
    remove_metadata,
    parse_task_string,
    create_task_from_string,
    parse_multiple_tasks
)
from src.models.task import Task


class TestExtractTags:
    """Tests for tag extraction."""
    
    def test_extract_single_tag(self):
        """Test extracting single tag."""
        assert extract_tags("Buy milk @shopping") == ["shopping"]
    
    def test_extract_multiple_tags(self):
        """Test extracting multiple tags."""
        tags = extract_tags("Task @work @urgent @coding")
        assert set(tags) == {"work", "urgent", "coding"}
    
    def test_extract_no_tags(self):
        """Test text with no tags."""
        assert extract_tags("Just a regular task") == []
    
    def test_extract_case_insensitive(self):
        """Test tag extraction is case insensitive."""
        assert extract_tags("Task @SHOPPING") == ["shopping"]


class TestExtractPriority:
    """Tests for priority extraction."""
    
    def test_extract_high_priority(self):
        """Test extracting high priority."""
        assert extract_priority("Task #high") == "high"
    
    def test_extract_medium_priority(self):
        """Test extracting medium priority."""
        assert extract_priority("Task #medium") == "medium"
    
    def test_extract_low_priority(self):
        """Test extracting low priority."""
        assert extract_priority("Task #low") == "low"
    
    def test_extract_no_priority(self):
        """Test text with no priority."""
        assert extract_priority("Just a task") is None
    
    def test_extract_case_insensitive(self):
        """Test priority extraction is case insensitive."""
        assert extract_priority("Task #HIGH") == "high"


class TestExtractDueDate:
    """Tests for due date extraction."""
    
    def test_extract_exact_date(self):
        """Test extracting exact date."""
        assert extract_due_date("Task due:2025-10-20") == "2025-10-20"
    
    def test_extract_relative_date(self):
        """Test extracting relative date."""
        from datetime import datetime, timedelta
        tomorrow = (datetime.now().date() + timedelta(days=1)).isoformat()
        assert extract_due_date("Task due:tomorrow") == tomorrow
    
    def test_extract_no_due_date(self):
        """Test text with no due date."""
        assert extract_due_date("Just a task") is None


class TestExtractEmail:
    """Tests for email extraction."""
    
    def test_extract_valid_email(self):
        """Test extracting valid email."""
        assert extract_email("Task assigned:alice@example.com") == "alice@example.com"
    
    def test_extract_email_lowercase(self):
        """Test email is converted to lowercase."""
        assert extract_email("Task assigned:Alice@Example.COM") == "alice@example.com"
    
    def test_extract_no_email(self):
        """Test text with no email."""
        assert extract_email("Just a task") is None


class TestExtractTime:
    """Tests for time extraction."""
    
    def test_extract_time_pm(self):
        """Test extracting PM time."""
        assert extract_time("Meeting at 3pm") == "15:00"
    
    def test_extract_time_am(self):
        """Test extracting AM time."""
        assert extract_time("Call by 9am") == "09:00"
    
    def test_extract_time_with_minutes(self):
        """Test extracting time with minutes."""
        assert extract_time("Deadline at 3:30pm") == "15:30"
    
    def test_extract_no_time(self):
        """Test text with no time."""
        assert extract_time("Just a task") is None


class TestExtractDuration:
    """Tests for duration extraction."""
    
    def test_extract_hours(self):
        """Test extracting hours duration."""
        result = extract_duration("Meeting 2h")
        assert result == "2h"
    
    def test_extract_minutes(self):
        """Test extracting minutes duration."""
        result = extract_duration("Call 30m")
        assert result == "30m"
    
    def test_extract_hours_and_minutes(self):
        """Test extracting hours and minutes."""
        result = extract_duration("Meeting 1h30m")
        assert result == "1h30m"
    
    def test_extract_no_duration(self):
        """Test text with no duration."""
        assert extract_duration("Just a task") is None


class TestRemoveMetadata:
    """Tests for metadata removal."""
    
    def test_remove_tags(self):
        """Test removing tags."""
        assert remove_metadata("Buy milk @shopping") == "Buy milk"
    
    def test_remove_priority(self):
        """Test removing priority."""
        assert remove_metadata("Task #high") == "Task"
    
    def test_remove_due_date(self):
        """Test removing due date."""
        assert remove_metadata("Task due:2025-10-20") == "Task"
    
    def test_remove_all_metadata(self):
        """Test removing all metadata."""
        text = "Buy milk @shopping #high due:2025-10-20 assigned:alice@example.com at 3pm"
        assert remove_metadata(text) == "Buy milk"
    
    def test_remove_extra_whitespace(self):
        """Test removing extra whitespace."""
        assert remove_metadata("  Buy   milk  @shopping") == "Buy milk"


class TestParseTaskString:
    """Tests for complete task string parsing."""
    
    def test_parse_minimal_task(self):
        """Test parsing minimal task."""
        result = parse_task_string("Buy milk")
        assert result['description'] == "Buy milk"
        assert result['tags'] == []
        assert result['priority'] is None
    
    def test_parse_complete_task(self):
        """Test parsing complete task with all components."""
        result = parse_task_string(
            "Buy groceries @shopping #high due:2025-10-20 assigned:alice@example.com at 3pm"
        )
        
        assert result['description'] == "Buy groceries"
        assert "shopping" in result['tags']
        assert result['priority'] == "high"
        assert result['due_date'] == "2025-10-20"
        assert result['assigned_to'] == "alice@example.com"
        assert result['time'] == "15:00"
    
    def test_parse_task_with_multiple_tags(self):
        """Test parsing task with multiple tags."""
        result = parse_task_string("Complete report @work @urgent @coding")
        assert len(result['tags']) == 3
        assert set(result['tags']) == {"work", "urgent", "coding"}
    
    def test_parse_empty_string(self):
        """Test parsing empty string raises error."""
        with pytest.raises(ValueError, match="empty"):
            parse_task_string("")
    
    def test_parse_only_metadata(self):
        """Test parsing string with only metadata raises error."""
        with pytest.raises(ValueError, match="description"):
            parse_task_string("@shopping #high")
    
    def test_parse_invalid_email(self):
        """Test parsing with invalid email raises error."""
        with pytest.raises(ValueError, match="email"):
            parse_task_string("Task assigned:not-an-email")
    
    def test_parse_invalid_priority(self):
        """Test parsing with invalid priority raises error."""
        with pytest.raises(ValueError, match="priority"):
            parse_task_string("Task #critical")


class TestCreateTaskFromString:
    """Tests for creating Task objects from strings."""
    
    def test_create_minimal_task(self):
        """Test creating minimal task."""
        task = create_task_from_string("Buy milk")
        
        assert isinstance(task, Task)
        assert task.description == "Buy milk"
        assert task.status == "incomplete"
    
    def test_create_complete_task(self):
        """Test creating complete task."""
        task = create_task_from_string(
            "Buy groceries @shopping #high due:2025-10-20 assigned:alice@example.com"
        )
        
        assert task.description == "Buy groceries"
        assert "shopping" in task.tags
        assert task.priority == "high"
        assert task.due_date == "2025-10-20"
        assert task.assigned_to == "alice@example.com"
    
    def test_create_task_with_relative_date(self):
        """Test creating task with relative date."""
        from datetime import datetime, timedelta
        tomorrow = (datetime.now().date() + timedelta(days=1)).isoformat()
        
        task = create_task_from_string("Call client due:tomorrow")
        assert task.due_date == tomorrow
    
    def test_create_task_with_time(self):
        """Test creating task with time."""
        task = create_task_from_string("Meeting at 3pm @work")
        assert task.time == "15:00"
    
    def test_create_task_has_id(self):
        """Test created task has auto-generated ID."""
        task = create_task_from_string("Buy milk")
        assert task.id is not None
        assert len(task.id) > 0
    
    def test_create_task_has_timestamps(self):
        """Test created task has timestamps."""
        task = create_task_from_string("Buy milk")
        assert task.created_at is not None
        assert task.updated_at is not None


class TestParseMultipleTasks:
    """Tests for parsing multiple tasks."""
    
    def test_parse_multiple_valid_tasks(self):
        """Test parsing multiple valid tasks."""
        tasks = parse_multiple_tasks([
            "Buy milk @shopping",
            "Review code @work #high",
            "Call client due:tomorrow"
        ])
        
        assert len(tasks) == 3
        assert all(isinstance(t, Task) for t in tasks)
    
    def test_parse_with_some_invalid(self):
        """Test parsing with some invalid tasks."""
        tasks = parse_multiple_tasks([
            "Buy milk @shopping",
            "@shopping #high",  # Invalid - no description
            "Review code @work"
        ])
        
        # Should only create valid tasks
        assert len(tasks) == 2
    
    def test_parse_empty_list(self):
        """Test parsing empty list."""
        tasks = parse_multiple_tasks([])
        assert tasks == []


class TestIntegration:
    """Integration tests with realistic scenarios."""
    
    def test_realistic_task_1(self):
        """Test realistic task: shopping with deadline."""
        task = create_task_from_string(
            "Buy groceries for dinner @shopping #high due:tomorrow at 5pm"
        )
        
        assert "Buy groceries for dinner" in task.description
        assert "shopping" in task.tags
        assert task.priority == "high"
        assert task.time == "17:00"
    
    def test_realistic_task_2(self):
        """Test realistic task: work assignment."""
        task = create_task_from_string(
            "Review PR #42 @coding @work #medium due:2025-10-20 assigned:bob@company.com"
        )
        
        assert "Review PR #42" in task.description
        assert "coding" in task.tags
        assert "work" in task.tags
        assert task.priority == "medium"
        assert task.assigned_to == "bob@company.com"
    
    def test_realistic_task_3(self):
        """Test realistic task: simple reminder."""
        task = create_task_from_string("Call mom")
        
        assert task.description == "Call mom"
        assert task.tags == []
        assert task.priority is None
    
    def test_task_with_numbers_in_description(self):
        """Test task with numbers in description."""
        task = create_task_from_string("Complete project phase 2 @work")
        assert "Complete project phase 2" in task.description