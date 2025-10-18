"""
Unit tests for task service.
"""

import pytest
from src.models.task import Task
from src.services.task_service import TaskService


@pytest.fixture
def task_service():
    """Create task service for testing."""
    service = TaskService("data/test_service_tasks.json")
    yield service
    # Cleanup
    if service.storage.file_exists():
        service.storage.delete_file()


class TestTaskService:
    """Task service tests."""
    
    def test_add_task_from_string(self, task_service):
        """Test adding task from string."""
        task_id = task_service.add_task_from_string(
            "Buy milk @shopping #high"
        )
        
        assert task_id is not None
        task = task_service.get_task(task_id)
        assert task.description == "Buy milk"
        assert "shopping" in task.tags
        assert task.priority == "high"
    
    def test_add_task_object(self, task_service):
        """Test adding task object."""
        task = Task(description="Buy milk")
        task_id = task_service.add_task(task)
        
        assert task_id is not None
        retrieved = task_service.get_task(task_id)
        assert retrieved.description == "Buy milk"
    
    def test_persistence(self, task_service):
        """Test tasks persist between sessions."""
        # Add task
        task_id = task_service.add_task_from_string("Buy milk")
        
        # Create new service instance (simulates restart)
        new_service = TaskService("data/test_service_tasks.json")
        
        # Task should still exist
        task = new_service.get_task(task_id)
        assert task is not None
        assert task.description == "Buy milk"
    
    def test_update_task(self, task_service):
        """Test updating task."""
        task_id = task_service.add_task_from_string("Buy milk")
        
        success = task_service.update_task(task_id, priority="high")
        assert success is True
        
        task = task_service.get_task(task_id)
        assert task.priority == "high"
    
    def test_delete_task(self, task_service):
        """Test deleting task."""
        task_id = task_service.add_task_from_string("Buy milk")
        
        success = task_service.delete_task(task_id)
        assert success is True
        
        task = task_service.get_task(task_id)
        assert task is None
    
    def test_mark_complete(self, task_service):
        """Test marking complete."""
        task_id = task_service.add_task_from_string("Buy milk")
        
        success = task_service.mark_complete(task_id)
        assert success is True
        
        task = task_service.get_task(task_id)
        assert task.is_complete is True
    
    def test_list_operations(self, task_service):
        """Test list operations."""
        task_service.add_task_from_string("Task 1 @work")
        task_service.add_task_from_string("Task 2 #high")
        
        all_tasks = task_service.list_all()
        assert len(all_tasks) == 2
        
        work_tasks = task_service.list_by_tag("work")
        assert len(work_tasks) == 1
        
        high_tasks = task_service.list_by_priority("high")
        assert len(high_tasks) == 1
    
    def test_search_tasks(self, task_service):
        """Test searching tasks."""
        task_service.add_task_from_string("Buy milk")
        task_service.add_task_from_string("Buy groceries")
        task_service.add_task_from_string("Call dentist")
        
        results = task_service.search_tasks("buy")
        assert len(results) == 2
        
        results = task_service.search_tasks("dentist")
        assert len(results) == 1
    
    def test_count_operations(self, task_service):
        """Test count operations."""
        task_service.add_task_from_string("Task 1")
        task_id = task_service.add_task_from_string("Task 2")
        task_service.mark_complete(task_id)
        
        assert task_service.count_all() == 2
        assert task_service.count_complete() == 1
        assert task_service.count_incomplete() == 1
    
    def test_clear_complete(self, task_service):
        """Test clearing complete tasks."""
        task_id = task_service.add_task_from_string("Task 1")
        task_service.mark_complete(task_id)
        task_service.add_task_from_string("Task 2")
        
        task_service.clear_complete()
        
        assert task_service.count_all() == 1
        assert task_service.count_complete() == 0