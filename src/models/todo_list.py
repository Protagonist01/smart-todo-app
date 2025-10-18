"""
TodoList class for managing a collection of tasks.
"""

from typing import List, Optional, Dict
from src.models.task import Task


class TodoList:
    """
    Manages a collection of tasks with CRUD operations.
    
    Attributes:
        tasks: Dictionary mapping task IDs to Task objects
    """
    
    def __init__(self):
        """Initialize empty todo list."""
        self.tasks: Dict[str, Task] = {}
    
    def add_task(self, task: Task) -> str:
        """
        Add a task to the list.
        
        Args:
            task: Task object to add
            
        Returns:
            Task ID
        """
        self.tasks[task.id] = task
        return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task object or None if not found
        """
        return self.tasks.get(task_id)
    
    def update_task(self, task_id: str, **updates) -> bool:
        """
        Update a task's attributes.
        
        Args:
            task_id: ID of the task to update
            **updates: Keyword arguments of attributes to update
            
        Returns:
            True if updated, False if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return False
        
        from datetime import datetime
        
        # Update allowed attributes
        allowed = ['description', 'tags', 'priority', 'due_date', 
                   'assigned_to', 'status', 'time', 'duration']
        
        for key, value in updates.items():
            if key in allowed:
                setattr(task, key, value)
        
        task.updated_at = datetime.now().isoformat()
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if deleted, False if not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def mark_complete(self, task_id: str) -> bool:
        """
        Mark a task as complete.
        
        Args:
            task_id: ID of the task
            
        Returns:
            True if marked, False if not found
        """
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            return True
        return False
    
    def mark_incomplete(self, task_id: str) -> bool:
        """
        Mark a task as incomplete.
        
        Args:
            task_id: ID of the task
            
        Returns:
            True if marked, False if not found
        """
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            return True
        return False
    
    def list_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return list(self.tasks.values())
    
    def list_incomplete_tasks(self) -> List[Task]:
        """
        Get all incomplete tasks.
        
        Returns:
            List of incomplete tasks
        """
        return [t for t in self.tasks.values() if not t.is_complete]
    
    def list_complete_tasks(self) -> List[Task]:
        """
        Get all complete tasks.
        
        Returns:
            List of complete tasks
        """
        return [t for t in self.tasks.values() if t.is_complete]
    
    def list_by_priority(self, priority: str) -> List[Task]:
        """
        Get tasks by priority level.
        
        Args:
            priority: Priority level (high/medium/low)
            
        Returns:
            List of tasks with specified priority
        """
        return [t for t in self.tasks.values() if t.priority == priority.lower()]
    
    def list_by_tag(self, tag: str) -> List[Task]:
        """
        Get tasks with a specific tag.
        
        Args:
            tag: Tag to filter by
            
        Returns:
            List of tasks with the tag
        """
        tag = tag.lower()
        return [t for t in self.tasks.values() if tag in t.tags]
    
    def list_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks.
        
        Returns:
            List of overdue tasks
        """
        return [t for t in self.tasks.values() if t.is_overdue]
    
    def count_tasks(self) -> int:
        """
        Count total tasks.
        
        Returns:
            Number of tasks
        """
        return len(self.tasks)
    
    def count_complete(self) -> int:
        """
        Count complete tasks.
        
        Returns:
            Number of complete tasks
        """
        return len(self.list_complete_tasks())
    
    def count_incomplete(self) -> int:
        """
        Count incomplete tasks.
        
        Returns:
            Number of incomplete tasks
        """
        return len(self.list_incomplete_tasks())
    
    def clear_all(self) -> None:
        """Clear all tasks."""
        self.tasks.clear()
    
    def clear_complete(self) -> None:
        """Delete all completed tasks."""
        complete_ids = [t.id for t in self.list_complete_tasks()]
        for task_id in complete_ids:
            self.delete_task(task_id)
    
    def to_dict(self) -> Dict:
        """
        Convert todo list to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'tasks': {task_id: task.to_dict() for task_id, task in self.tasks.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TodoList':
        """
        Create TodoList from dictionary.
        
        Args:
            data: Dictionary with task data
            
        Returns:
            New TodoList instance
        """
        todo_list = cls()
        if 'tasks' in data:
            for task_id, task_data in data['tasks'].items():
                task = Task.from_dict(task_data)
                todo_list.tasks[task_id] = task
        return todo_list