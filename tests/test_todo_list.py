"""
Unit tests for TodoList class.
"""

import pytest
from src.models.task import Task
from src.models.todo_list import TodoList


class TestTodoListBasics:
    """Basic TodoList operations."""
    
    def test_create_empty_list(self):
        """Test creating empty list."""
        todo = TodoList()
        assert todo.count_tasks() == 0
    
    def test_add_task(self):
        """Test adding task."""
        todo = TodoList()
        task = Task(description="Buy milk")
        task_id = todo.add_task(task)
        
        assert todo.count_tasks() == 1
        assert task_id == task.id
    
    def test_get_task(self):
        """Test getting task by ID."""
        todo = TodoList()
        task = Task(description="Buy milk")
        task_id = todo.add_task(task)
        
        retrieved = todo.get_task(task_id)
        assert retrieved is not None
        assert retrieved.description == "Buy milk"
    
    def test_get_nonexistent_task(self):
        """Test getting non-existent task."""
        todo = TodoList()
        assert todo.get_task("fake-id") is None


class TestCRUDOperations:
    """CRUD operation tests."""
    
    def test_update_task(self):
        """Test updating task."""
        todo = TodoList()
        task = Task(description="Buy milk", priority="low")
        task_id = todo.add_task(task)
        
        success = todo.update_task(task_id, priority="high", description="Buy groceries")
        assert success is True
        
        updated = todo.get_task(task_id)
        assert updated.priority == "high"
        assert updated.description == "Buy groceries"
    
    def test_update_nonexistent_task(self):
        """Test updating non-existent task."""
        todo = TodoList()
        success = todo.update_task("fake-id", priority="high")
        assert success is False
    
    def test_delete_task(self):
        """Test deleting task."""
        todo = TodoList()
        task = Task(description="Buy milk")
        task_id = todo.add_task(task)
        
        success = todo.delete_task(task_id)
        assert success is True
        assert todo.count_tasks() == 0
    
    def test_delete_nonexistent_task(self):
        """Test deleting non-existent task."""
        todo = TodoList()
        success = todo.delete_task("fake-id")
        assert success is False
    
    def test_mark_complete(self):
        """Test marking task complete."""
        todo = TodoList()
        task = Task(description="Buy milk")
        task_id = todo.add_task(task)
        
        success = todo.mark_complete(task_id)
        assert success is True
        
        task = todo.get_task(task_id)
        assert task.is_complete is True
    
    def test_mark_incomplete(self):
        """Test marking task incomplete."""
        todo = TodoList()
        task = Task(description="Buy milk", status="complete")
        task_id = todo.add_task(task)
        
        success = todo.mark_incomplete(task_id)
        assert success is True
        
        task = todo.get_task(task_id)
        assert task.is_complete is False


class TestListOperations:
    """List and filter operations."""
    
    def test_list_all_tasks(self):
        """Test listing all tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1"))
        todo.add_task(Task(description="Task 2"))
        
        tasks = todo.list_all_tasks()
        assert len(tasks) == 2
    
    def test_list_incomplete_tasks(self):
        """Test listing incomplete tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", status="incomplete"))
        todo.add_task(Task(description="Task 2", status="complete"))
        
        tasks = todo.list_incomplete_tasks()
        assert len(tasks) == 1
    
    def test_list_complete_tasks(self):
        """Test listing complete tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", status="incomplete"))
        todo.add_task(Task(description="Task 2", status="complete"))
        
        tasks = todo.list_complete_tasks()
        assert len(tasks) == 1
    
    def test_list_by_priority(self):
        """Test filtering by priority."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", priority="high"))
        todo.add_task(Task(description="Task 2", priority="low"))
        
        high = todo.list_by_priority("high")
        assert len(high) == 1
        assert high[0].priority == "high"
    
    def test_list_by_tag(self):
        """Test filtering by tag."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", tags=["work", "urgent"]))
        todo.add_task(Task(description="Task 2", tags=["personal"]))
        
        work_tasks = todo.list_by_tag("work")
        assert len(work_tasks) == 1
    
    def test_list_overdue_tasks(self):
        """Test listing overdue tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Old", due_date="2020-01-01"))
        todo.add_task(Task(description="Future", due_date="2030-01-01"))
        
        overdue = todo.list_overdue_tasks()
        assert len(overdue) == 1


class TestCountOperations:
    """Count operations."""
    
    def test_count_tasks(self):
        """Test counting tasks."""
        todo = TodoList()
        assert todo.count_tasks() == 0
        
        todo.add_task(Task(description="Task 1"))
        assert todo.count_tasks() == 1
    
    def test_count_complete(self):
        """Test counting complete tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", status="complete"))
        todo.add_task(Task(description="Task 2", status="incomplete"))
        
        assert todo.count_complete() == 1
    
    def test_count_incomplete(self):
        """Test counting incomplete tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", status="complete"))
        todo.add_task(Task(description="Task 2", status="incomplete"))
        
        assert todo.count_incomplete() == 1


class TestClearOperations:
    """Clear operations."""
    
    def test_clear_all(self):
        """Test clearing all tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1"))
        todo.add_task(Task(description="Task 2"))
        
        todo.clear_all()
        assert todo.count_tasks() == 0
    
    def test_clear_complete(self):
        """Test clearing complete tasks only."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", status="complete"))
        todo.add_task(Task(description="Task 2", status="incomplete"))
        
        todo.clear_complete()
        assert todo.count_tasks() == 1
        assert todo.count_incomplete() == 1


class TestSerialization:
    """Serialization tests."""
    
    def test_to_dict(self):
        """Test converting to dict."""
        todo = TodoList()
        task = Task(description="Buy milk", priority="high")
        todo.add_task(task)
        
        data = todo.to_dict()
        assert 'tasks' in data
        assert len(data['tasks']) == 1
    
    def test_from_dict(self):
        """Test creating from dict."""
        data = {
            'tasks': {
                'task-1': {
                    'id': 'task-1',
                    'description': 'Buy milk',
                    'tags': [],
                    'priority': 'high',
                    'due_date': None,
                    'assigned_to': None,
                    'status': 'incomplete',
                    'created_at': '2025-10-17T10:00:00',
                    'updated_at': '2025-10-17T10:00:00',
                    'time': None,
                    'duration': None
                }
            }
        }
        
        todo = TodoList.from_dict(data)
        assert todo.count_tasks() == 1
        
        task = todo.get_task('task-1')
        assert task.description == 'Buy milk'
    
    def test_round_trip_serialization(self):
        """Test to_dict and from_dict preserve data."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", priority="high"))
        todo.add_task(Task(description="Task 2", tags=["work"]))
        
        data = todo.to_dict()
        restored = TodoList.from_dict(data)
        
        assert restored.count_tasks() == 2