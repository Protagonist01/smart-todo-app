"""
Storage service for persisting tasks to JSON file.
"""

import json
import os
from typing import Optional
from pathlib import Path
from src.models.todo_list import TodoList


class StorageService:
    """
    Handles saving and loading tasks from JSON file.
    
    Attributes:
        file_path: Path to the JSON storage file
    """
    
    def __init__(self, file_path: str = "data/tasks.json"):
        """
        Initialize storage service.
        
        Args:
            file_path: Path to JSON file for storage
        """
        self.file_path = file_path
        self._ensure_data_directory()
    
    def _ensure_data_directory(self) -> None:
        """Create data directory if it doesn't exist."""
        directory = os.path.dirname(self.file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
    
    def save(self, todo_list: TodoList) -> bool:
        """
        Save todo list to JSON file.
        
        Args:
            todo_list: TodoList to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = todo_list.to_dict()
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def load(self) -> Optional[TodoList]:
        """
        Load todo list from JSON file.
        
        Returns:
            TodoList object or None if file doesn't exist or error occurs
        """
        if not os.path.exists(self.file_path):
            return TodoList()  # Return empty list if file doesn't exist
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return TodoList.from_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return None
    
    def file_exists(self) -> bool:
        """
        Check if storage file exists.
        
        Returns:
            True if file exists, False otherwise
        """
        return os.path.exists(self.file_path)
    
    def delete_file(self) -> bool:
        """
        Delete the storage file.
        
        Returns:
            True if deleted, False if file doesn't exist
        """
        if self.file_exists():
            try:
                os.remove(self.file_path)
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        return False
    
    def get_file_size(self) -> int:
        """
        Get size of storage file in bytes.
        
        Returns:
            File size in bytes, or 0 if file doesn't exist
        """
        if self.file_exists():
            return os.path.getsize(self.file_path)
        return 0
    
    def backup(self, backup_path: Optional[str] = None) -> bool:
        """
        Create a backup of the current storage file.
        
        Args:
            backup_path: Optional custom backup path
            
        Returns:
            True if backup successful, False otherwise
        """
        if not self.file_exists():
            return False
        
        try:
            if backup_path is None:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{self.file_path}.backup_{timestamp}"
            
            import shutil
            shutil.copy2(self.file_path, backup_path)
            return True
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """
        Restore tasks from a backup file.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if restore successful, False otherwise
        """
        if not os.path.exists(backup_path):
            return False
        
        try:
            import shutil
            shutil.copy2(backup_path, self.file_path)
            return True
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False