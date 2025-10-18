"""
Task service that combines TodoList with storage.
"""

from typing import List, Optional
from src.models.task import Task
from src.models.todo_list import TodoList
from src.services.storage_service import StorageService
from src.parsers.task_parser import create_task_from_string


class TaskService:
    """
    High-level service for task management with automatic persistence.
    """
    
    def __init__(self, storage_path: str = "data/tasks.json"):
        """
        Initialize task service.
        
        Args:
            storage_path: Path to storage file
        """
        self.storage = StorageService(storage_path)
        self.todo_list = self.storage.load() or TodoList()
    
    def _save(self) -> bool:
        """Save current state to storage."""
        return self.storage.save(self.todo_list)
    
    def add_task_from_string(self, task_string: str) -> Optional[str]:
        """
        Parse and add task from string.
        
        Args:
            task_string: Natural language task string
            
        Returns:
            Task ID if successful, None otherwise
        """
        try:
            task = create_task_from_string(task_string)
            task_id = self.todo_list.add_task(task)
            self._save()
            return task_id
        except Exception as e:
            print(f"Error adding task: {e}")
            return None
    
    def add_task(self, task: Task) -> str:
        """
        Add a task object.
        
        Args:
            task: Task object to add
            
        Returns:
            Task ID
        """
        task_id = self.todo_list.add_task(task)
        self._save()
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        return self.todo_list.get_task(task_id)
    
    def update_task(self, task_id: str, **updates) -> bool:
        """Update task and save."""
        success = self.todo_list.update_task(task_id, **updates)
        if success:
            self._save()
        return success
    
    def delete_task(self, task_id: str) -> bool:
        """Delete task and save."""
        success = self.todo_list.delete_task(task_id)
        if success:
            self._save()
        return success
    
    def mark_complete(self, task_id: str) -> bool:
        """Mark task complete and save."""
        success = self.todo_list.mark_complete(task_id)
        if success:
            self._save()
        return success
    
    def mark_incomplete(self, task_id: str) -> bool:
        """Mark task incomplete and save."""
        success = self.todo_list.mark_incomplete(task_id)
        if success:
            self._save()
        return success
    
    def list_all(self) -> List[Task]:
        """List all tasks."""
        return self.todo_list.list_all_tasks()
    
    def list_incomplete(self) -> List[Task]:
        """List incomplete tasks."""
        return self.todo_list.list_incomplete_tasks()
    
    def list_complete(self) -> List[Task]:
        """List complete tasks."""
        return self.todo_list.list_complete_tasks()
    
    def list_by_priority(self, priority: str) -> List[Task]:
        """List tasks by priority."""
        return self.todo_list.list_by_priority(priority)
    
    def list_by_tag(self, tag: str) -> List[Task]:
        """List tasks by tag."""
        return self.todo_list.list_by_tag(tag)
    
    def list_overdue(self) -> List[Task]:
        """List overdue tasks."""
        return self.todo_list.list_overdue_tasks()
    
    def search_tasks(self, keyword: str) -> List[Task]:
        """
        Search tasks by keyword in description.
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching tasks
        """
        keyword = keyword.lower()
        return [t for t in self.todo_list.list_all_tasks() 
                if keyword in t.description.lower()]
    
    def count_all(self) -> int:
        """Count all tasks."""
        return self.todo_list.count_tasks()
    
    def count_complete(self) -> int:
        """Count complete tasks."""
        return self.todo_list.count_complete()
    
    def count_incomplete(self) -> int:
        """Count incomplete tasks."""
        return self.todo_list.count_incomplete()
    
    def clear_complete(self) -> None:
        """Clear completed tasks and save."""
        self.todo_list.clear_complete()
        self._save()
    
    def clear_all(self) -> None:
        """Clear all tasks and save."""
        self.todo_list.clear_all()
        self._save()