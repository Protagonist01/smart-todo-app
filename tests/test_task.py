"""
Unit tests for Task model.
"""

import pytest
from datetime import datetime
from src.models.task import Task


class TestTaskCreation:
    """Tests for creating Task instances."""
    
    def test_create_minimal_task(self):
        """Test creating a task with only description."""
        task = Task(description="Buy milk")
        
        assert task.description == "Buy milk"
        assert task.status == "incomplete"
        assert task.tags == []
        assert task.priority is None
        assert task.id is not None  # Should auto-generate ID
    
    def test_create_full_task(self):
        """Test creating a task with all fields."""
        task = Task(
            description="Buy groceries",
            tags=["shopping", "urgent"],
            priority="high",
            due_date="2025-10-20",
            assigned_to="alice@example.com",
            time="14:00",
            duration="1h"
        )
        
        assert task.description == "Buy groceries"
        assert task.tags == ["shopping", "urgent"]
        assert task.priority == "high"
        assert task.due_date == "2025-10-20"
        assert task.assigned_to == "alice@example.com"
        assert task.time == "14:00"
        assert task.duration == "1h"
    
    def test_auto_generate_id(self):
        """Test that ID is auto-generated."""
        task1 = Task(description="Task 1")
        task2 = Task(description="Task 2")
        
        assert task1.id != task2.id
        assert len(task1.id) > 0
    
    def test_auto_generate_timestamps(self):
        """Test that timestamps are auto-generated."""
        task = Task(description="Buy milk")
        
        assert task.created_at is not None
        assert task.updated_at is not None
        
        # Should be valid ISO format timestamps
        datetime.fromisoformat(task.created_at)
        datetime.fromisoformat(task.updated_at)
    
    def test_normalize_priority(self):
        """Test that priority is normalized to lowercase."""
        task = Task(description="Task", priority="HIGH")
        assert task.priority == "high"
    
    def test_normalize_tags(self):
        """Test that tags are normalized to lowercase."""
        task = Task(description="Task", tags=["Shopping", "URGENT"])
        assert task.tags == ["shopping", "urgent"]
    
    def test_normalize_email(self):
        """Test that email is normalized to lowercase."""
        task = Task(description="Task", assigned_to="Alice@Example.COM")
        assert task.assigned_to == "alice@example.com"
    
    def test_invalid_priority_raises_error(self):
        """Test that invalid priority raises ValueError."""
        with pytest.raises(ValueError, match="Invalid priority"):
            Task(description="Task", priority="critical")
    
    def test_invalid_status_raises_error(self):
        """Test that invalid status raises ValueError."""
        with pytest.raises(ValueError, match="Invalid status"):
            Task(description="Task", status="pending")


class TestTaskMethods:
    """Tests for Task methods."""
    
    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(description="Buy milk")
        assert task.status == "incomplete"
        
        task.mark_complete()
        assert task.status == "complete"
    
    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        task = Task(description="Buy milk", status="complete")
        assert task.status == "complete"
        
        task.mark_incomplete()
        assert task.status == "incomplete"
    
    def test_mark_complete_updates_timestamp(self):
        """Test that marking complete updates timestamp."""
        task = Task(description="Buy milk")
        original_time = task.updated_at
        
        import time
        time.sleep(0.01)  # Small delay to ensure timestamp changes
        
        task.mark_complete()
        assert task.updated_at != original_time
    
    def test_add_tag(self):
        """Test adding a tag."""
        task = Task(description="Buy milk")
        task.add_tag("shopping")
        
        assert "shopping" in task.tags
    
    def test_add_duplicate_tag(self):
        """Test that duplicate tags are not added."""
        task = Task(description="Buy milk", tags=["shopping"])
        task.add_tag("shopping")
        
        assert task.tags.count("shopping") == 1
    
    def test_add_tag_normalizes(self):
        """Test that adding tag normalizes to lowercase."""
        task = Task(description="Buy milk")
        task.add_tag("SHOPPING")
        
        assert "shopping" in task.tags
        assert "SHOPPING" not in task.tags
    
    def test_remove_tag(self):
        """Test removing a tag."""
        task = Task(description="Buy milk", tags=["shopping", "urgent"])
        task.remove_tag("urgent")
        
        assert "urgent" not in task.tags
        assert "shopping" in task.tags
    
    def test_remove_nonexistent_tag(self):
        """Test removing a tag that doesn't exist."""
        task = Task(description="Buy milk", tags=["shopping"])
        task.remove_tag("urgent")  # Should not raise error
        
        assert task.tags == ["shopping"]
    
    def test_update_priority(self):
        """Test updating priority."""
        task = Task(description="Buy milk", priority="low")
        task.update_priority("high")
        
        assert task.priority == "high"
    
    def test_update_priority_invalid(self):
        """Test that invalid priority raises error."""
        task = Task(description="Buy milk")
        
        with pytest.raises(ValueError):
            task.update_priority("critical")


class TestTaskSerialization:
    """Tests for converting Task to/from dict."""
    
    def test_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            description="Buy milk",
            tags=["shopping"],
            priority="high",
            due_date="2025-10-20"
        )
        
        data = task.to_dict()
        
        assert data['description'] == "Buy milk"
        assert data['tags'] == ["shopping"]
        assert data['priority'] == "high"
        assert data['due_date'] == "2025-10-20"
        assert 'id' in data
        assert 'created_at' in data
    
    def test_from_dict(self):
        """Test creating task from dictionary."""
        data = {
            'id': '123',
            'description': 'Buy milk',
            'tags': ['shopping'],
            'priority': 'high',
            'due_date': '2025-10-20',
            'status': 'incomplete',
            'created_at': '2025-10-16T10:00:00',
            'updated_at': '2025-10-16T10:00:00',
            'assigned_to': None,
            'time': None,
            'duration': None
        }
        
        task = Task.from_dict(data)
        
        assert task.id == '123'
        assert task.description == 'Buy milk'
        assert task.tags == ['shopping']
        assert task.priority == 'high'
    
    def test_round_trip_serialization(self):
        """Test converting to dict and back preserves data."""
        original = Task(
            description="Buy milk",
            tags=["shopping", "urgent"],
            priority="high"
        )
        
        data = original.to_dict()
        restored = Task.from_dict(data)
        
        assert restored.description == original.description
        assert restored.tags == original.tags
        assert restored.priority == original.priority
        assert restored.id == original.id


class TestTaskProperties:
    """Tests for Task properties."""
    
    def test_is_complete_property(self):
        """Test is_complete property."""
        task = Task(description="Buy milk", status="complete")
        assert task.is_complete is True
        
        task.mark_incomplete()
        assert task.is_complete is False
    
    def test_is_high_priority_property(self):
        """Test is_high_priority property."""
        task = Task(description="Buy milk", priority="high")
        assert task.is_high_priority is True
        
        task2 = Task(description="Buy milk", priority="low")
        assert task2.is_high_priority is False
    
    def test_is_overdue_property(self):
        """Test is_overdue property."""
        # Task with past due date
        task1 = Task(description="Buy milk", due_date="2020-01-01")
        assert task1.is_overdue is True
        
        # Task with future due date
        task2 = Task(description="Buy milk", due_date="2030-01-01")
        assert task2.is_overdue is False
        
        # Completed task is not overdue
        task3 = Task(description="Buy milk", due_date="2020-01-01", status="complete")
        assert task3.is_overdue is False
        
        # Task with no due date is not overdue
        task4 = Task(description="Buy milk")
        assert task4.is_overdue is False


class TestTaskStringRepresentation:
    """Tests for string representation of tasks."""
    
    def test_str_incomplete_task(self):
        """Test string representation of incomplete task."""
        task = Task(description="Buy milk", priority="high", tags=["shopping"])
        string = str(task)
        
        assert "Buy milk" in string
        assert "high" in string
        assert "shopping" in string
        assert "○" in string or "incomplete" in string.lower()
    
    def test_str_complete_task(self):
        """Test string representation of complete task."""
        task = Task(description="Buy milk", status="complete")
        string = str(task)
        
        assert "Buy milk" in string
        assert "✓" in string or "complete" in string.lower()
    
    def test_repr_task(self):
        """Test repr representation."""
        task = Task(description="Buy milk")
        repr_str = repr(task)
        
        assert "Task" in repr_str
        assert "Buy milk" in repr_str
        assert task.id in repr_str