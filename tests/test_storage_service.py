"""
Unit tests for storage service.
"""

import pytest
import os
import json
from src.models.task import Task
from src.models.todo_list import TodoList
from src.services.storage_service import StorageService


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    storage = StorageService("data/test_tasks.json")
    yield storage
    # Cleanup
    if storage.file_exists():
        storage.delete_file()


class TestStorageService:
    """Storage service tests."""
    
    def test_save_and_load(self, temp_storage):
        """Test saving and loading."""
        todo = TodoList()
        todo.add_task(Task(description="Buy milk", priority="high"))
        
        # Save
        success = temp_storage.save(todo)
        assert success is True
        assert temp_storage.file_exists() is True
        
        # Load
        loaded = temp_storage.load()
        assert loaded is not None
        assert loaded.count_tasks() == 1
        
        task = loaded.list_all_tasks()[0]
        assert task.description == "Buy milk"
        assert task.priority == "high"
    
    def test_load_nonexistent_file(self, temp_storage):
        """Test loading when file doesn't exist."""
        loaded = temp_storage.load()
        assert loaded is not None
        assert loaded.count_tasks() == 0
    
    def test_save_multiple_tasks(self, temp_storage):
        """Test saving multiple tasks."""
        todo = TodoList()
        todo.add_task(Task(description="Task 1", tags=["work"]))
        todo.add_task(Task(description="Task 2", priority="high"))
        todo.add_task(Task(description="Task 3", due_date="2025-10-20"))
        
        temp_storage.save(todo)
        loaded = temp_storage.load()
        
        assert loaded.count_tasks() == 3
    
    def test_file_exists(self, temp_storage):
        """Test file_exists method."""
        assert temp_storage.file_exists() is False
        
        todo = TodoList()
        temp_storage.save(todo)
        
        assert temp_storage.file_exists() is True
    
    def test_delete_file(self, temp_storage):
        """Test deleting file."""
        todo = TodoList()
        temp_storage.save(todo)
        
        assert temp_storage.file_exists() is True
        
        success = temp_storage.delete_file()
        assert success is True
        assert temp_storage.file_exists() is False
    
    def test_get_file_size(self, temp_storage):
        """Test getting file size."""
        assert temp_storage.get_file_size() == 0
        
        todo = TodoList()
        todo.add_task(Task(description="Buy milk"))
        temp_storage.save(todo)
        
        size = temp_storage.get_file_size()
        assert size > 0
    
    def test_backup_and_restore(self, temp_storage):
        """Test backup and restore."""
        todo = TodoList()
        todo.add_task(Task(description="Original task"))
        temp_storage.save(todo)
        
        # Backup
        backup_path = "data/test_backup.json"
        success = temp_storage.backup(backup_path)
        assert success is True
        
        # Modify original
        todo.add_task(Task(description="New task"))
        temp_storage.save(todo)
        
        # Restore
        success = temp_storage.restore_from_backup(backup_path)
        assert success is True
        
        loaded = temp_storage.load()
        assert loaded.count_tasks() == 1
        
        # Cleanup backup
        if os.path.exists(backup_path):
            os.remove(backup_path)