"""
Task data model.

This module defines the Task class which represents a single todo item.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid


@dataclass
class Task:
    """
    Represents a single todo task.
    
    Attributes:
        id: Unique identifier for the task
        description: Main text describing what needs to be done
        tags: List of category tags (e.g., ['shopping', 'urgent'])
        priority: Priority level ('high', 'medium', 'low', or None)
        due_date: Due date in YYYY-MM-DD format (optional)
        assigned_to: Email address of person assigned (optional)
        status: Current status ('incomplete' or 'complete')
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last modified
        time: Specific time for the task (optional, e.g., "14:00")
        duration: Expected duration (optional, e.g., "1h30m")
    
    Example:
        >>> task = Task(
        ...     description="Buy groceries",
        ...     tags=["shopping"],
        ...     priority="high",
        ...     due_date="2025-10-20"
        ... )
        >>> print(task.description)
        'Buy groceries'
    """
    
    # Required fields
    description: str
    
    # Optional fields with defaults
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tags: List[str] = field(default_factory=list)
    priority: Optional[str] = None
    due_date: Optional[str] = None
    assigned_to: Optional[str] = None
    status: str = "incomplete"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    time: Optional[str] = None
    duration: Optional[str] = None
    
    def __post_init__(self):
        """
        Validate and normalize data after initialization.
        """
        # Normalize priority to lowercase
        if self.priority:
            self.priority = self.priority.lower()
            if self.priority not in ['high', 'medium', 'low']:
                raise ValueError(f"Invalid priority: {self.priority}. Must be 'high', 'medium', or 'low'.")
        
        # Normalize status to lowercase
        self.status = self.status.lower()
        if self.status not in ['incomplete', 'complete']:
            raise ValueError(f"Invalid status: {self.status}. Must be 'incomplete' or 'complete'.")
        
        # Normalize tags to lowercase
        self.tags = [tag.lower() for tag in self.tags]
        
        # Normalize email to lowercase
        if self.assigned_to:
            self.assigned_to = self.assigned_to.lower()
    
    def mark_complete(self) -> None:
        """
        Mark the task as complete and update the timestamp.
        
        Example:
            >>> task = Task(description="Buy milk")
            >>> task.mark_complete()
            >>> task.status
            'complete'
        """
        self.status = "complete"
        self.updated_at = datetime.now().isoformat()
    
    def mark_incomplete(self) -> None:
        """
        Mark the task as incomplete and update the timestamp.
        
        Example:
            >>> task = Task(description="Buy milk", status="complete")
            >>> task.mark_incomplete()
            >>> task.status
            'incomplete'
        """
        self.status = "incomplete"
        self.updated_at = datetime.now().isoformat()
    
    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the task if it doesn't already exist.
        
        Args:
            tag: Tag to add (will be converted to lowercase)
        
        Example:
            >>> task = Task(description="Buy milk")
            >>> task.add_tag("shopping")
            >>> task.tags
            ['shopping']
        """
        tag = tag.lower()
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.now().isoformat()
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from the task if it exists.
        
        Args:
            tag: Tag to remove
        
        Example:
            >>> task = Task(description="Buy milk", tags=["shopping", "urgent"])
            >>> task.remove_tag("urgent")
            >>> task.tags
            ['shopping']
        """
        tag = tag.lower()
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.now().isoformat()
    
    def update_priority(self, priority: str) -> None:
        """
        Update the task priority.
        
        Args:
            priority: New priority level ('high', 'medium', or 'low')
        
        Raises:
            ValueError: If priority is invalid
        
        Example:
            >>> task = Task(description="Buy milk", priority="low")
            >>> task.update_priority("high")
            >>> task.priority
            'high'
        """
        priority = priority.lower()
        if priority not in ['high', 'medium', 'low']:
            raise ValueError(f"Invalid priority: {priority}")
        
        self.priority = priority
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of the task
        
        Example:
            >>> task = Task(description="Buy milk", tags=["shopping"])
            >>> data = task.to_dict()
            >>> data['description']
            'Buy milk'
        """
        return {
            'id': self.id,
            'description': self.description,
            'tags': self.tags,
            'priority': self.priority,
            'due_date': self.due_date,
            'assigned_to': self.assigned_to,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'time': self.time,
            'duration': self.duration,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task instance from a dictionary.
        
        Args:
            data: Dictionary containing task data
        
        Returns:
            New Task instance
        
        Example:
            >>> data = {
            ...     'description': 'Buy milk',
            ...     'tags': ['shopping'],
            ...     'priority': 'high'
            ... }
            >>> task = Task.from_dict(data)
            >>> task.description
            'Buy milk'
        """
        return cls(**data)
    
    def __str__(self) -> str:
        """
        Return a human-readable string representation of the task.
        
        Example:
            >>> task = Task(description="Buy milk", priority="high", tags=["shopping"])
            >>> print(task)
            [incomplete] Buy milk
            Priority: high | Tags: shopping | Due: None
        """
        status_symbol = "✓" if self.status == "complete" else "○"
        tags_str = ", ".join(self.tags) if self.tags else "None"
        priority_str = self.priority if self.priority else "None"
        due_str = self.due_date if self.due_date else "None"
        
        result = f"[{status_symbol}] {self.description}\n"
        result += f"    Priority: {priority_str} | Tags: {tags_str} | Due: {due_str}"
        
        if self.assigned_to:
            result += f" | Assigned: {self.assigned_to}"
        
        if self.time:
            result += f" | Time: {self.time}"
        
        return result
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation for debugging.
        
        Example:
            >>> task = Task(description="Buy milk")
            >>> repr(task)
            "Task(id='...', description='Buy milk', status='incomplete')"
        """
        return (f"Task(id='{self.id}', description='{self.description}', "
                f"status='{self.status}', priority='{self.priority}')")
    
    @property
    def is_complete(self) -> bool:
        """
        Check if the task is complete.
        
        Returns:
            True if task is complete, False otherwise
        
        Example:
            >>> task = Task(description="Buy milk", status="complete")
            >>> task.is_complete
            True
        """
        return self.status == "complete"
    
    @property
    def is_overdue(self) -> bool:
        """
        Check if the task is overdue.
        
        Returns:
            True if task has a due date in the past and is incomplete
        
        Example:
            >>> task = Task(description="Buy milk", due_date="2020-01-01")
            >>> task.is_overdue
            True
        """
        if not self.due_date or self.is_complete:
            return False
        
        try:
            due = datetime.fromisoformat(self.due_date)
            return due.date() < datetime.now().date()
        except (ValueError, TypeError):
            return False
    
    @property
    def is_high_priority(self) -> bool:
        """
        Check if the task is high priority.
        
        Returns:
            True if priority is 'high'
        
        Example:
            >>> task = Task(description="Buy milk", priority="high")
            >>> task.is_high_priority
            True
        """
        return self.priority == "high"