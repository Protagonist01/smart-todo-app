"""
Validation functions for task components.

This module provides functions to validate various task attributes
like emails, dates, priorities, and tags.
"""

import re
from datetime import datetime
from typing import Tuple, List


def validate_email(email: str) -> bool:
    """
    Validate an email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid, False otherwise
        
    Example:
        >>> validate_email("alice@example.com")
        True
        >>> validate_email("invalid-email")
        False
    """
    if not email:
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_priority(priority: str) -> bool:
    """
    Validate a priority level.
    
    Args:
        priority: Priority level to validate
        
    Returns:
        True if priority is valid (high, medium, low), False otherwise
        
    Example:
        >>> validate_priority("high")
        True
        >>> validate_priority("critical")
        False
    """
    if not priority:
        return False
    
    valid_priorities = ['high', 'medium', 'low']
    return priority.lower() in valid_priorities


def validate_date_format(date_string: str) -> bool:
    """
    Validate a date string is in YYYY-MM-DD format.
    
    Args:
        date_string: Date string to validate
        
    Returns:
        True if date format is valid, False otherwise
        
    Example:
        >>> validate_date_format("2025-10-20")
        True
        >>> validate_date_format("10/20/2025")
        False
    """
    if not date_string:
        return False
    
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def validate_date_not_past(date_string: str) -> bool:
    """
    Validate that a date is not in the past.
    
    Args:
        date_string: Date string in YYYY-MM-DD format
        
    Returns:
        True if date is today or in the future, False otherwise
        
    Example:
        >>> validate_date_not_past("2030-01-01")
        True
        >>> validate_date_not_past("2020-01-01")
        False
    """
    if not validate_date_format(date_string):
        return False
    
    try:
        date = datetime.strptime(date_string, '%Y-%m-%d').date()
        today = datetime.now().date()
        return date >= today
    except ValueError:
        return False


def validate_tag(tag: str) -> bool:
    """
    Validate a tag format.
    
    Tags should be alphanumeric with optional underscores.
    
    Args:
        tag: Tag to validate
        
    Returns:
        True if tag is valid, False otherwise
        
    Example:
        >>> validate_tag("shopping")
        True
        >>> validate_tag("work_2024")
        True
        >>> validate_tag("@invalid")
        False
    """
    if not tag:
        return False
    
    # Tags should be alphanumeric with optional underscores
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, tag) is not None


def validate_time_format(time_string: str) -> bool:
    """
    Validate a time string format.
    
    Accepts formats like: "14:00", "3pm", "3:30pm"
    
    Args:
        time_string: Time string to validate
        
    Returns:
        True if time format is valid, False otherwise
        
    Example:
        >>> validate_time_format("14:00")
        True
        >>> validate_time_format("3pm")
        True
        >>> validate_time_format("25:00")
        False
    """
    if not time_string:
        return False
    
    # Pattern for HH:MM or H:MM or Hpm/Ham
    patterns = [
        r'^\d{1,2}:\d{2}$',  # 14:00, 3:30
        r'^\d{1,2}(am|pm)$',  # 3pm, 11am
        r'^\d{1,2}:\d{2}(am|pm)$'  # 3:30pm
    ]
    
    for pattern in patterns:
        if re.match(pattern, time_string.lower()):
            # Validate hour is 0-23 or 1-12 for am/pm
            try:
                if ':' in time_string:
                    hour = int(time_string.split(':')[0])
                else:
                    hour = int(re.match(r'\d+', time_string).group())
                
                if 'am' in time_string.lower() or 'pm' in time_string.lower():
                    return 1 <= hour <= 12
                else:
                    return 0 <= hour <= 23
            except (ValueError, AttributeError):
                return False
    
    return False


def validate_task_data(task_dict: dict) -> Tuple[bool, List[str]]:
    """
    Validate all components of a task dictionary.
    
    Args:
        task_dict: Dictionary containing task data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
        
    Example:
        >>> data = {'description': 'Buy milk', 'priority': 'high'}
        >>> valid, errors = validate_task_data(data)
        >>> valid
        True
        >>> errors
        []
    """
    errors = []
    
    # Validate description (required)
    if 'description' not in task_dict or not task_dict['description']:
        errors.append("Task description is required")
    elif not task_dict['description'].strip():
        errors.append("Task description cannot be empty")
    
    # Validate priority (if provided)
    if 'priority' in task_dict and task_dict['priority']:
        if not validate_priority(task_dict['priority']):
            errors.append(f"Invalid priority: {task_dict['priority']}. Must be 'high', 'medium', or 'low'")
    
    # Validate email (if provided)
    if 'assigned_to' in task_dict and task_dict['assigned_to']:
        if not validate_email(task_dict['assigned_to']):
            errors.append(f"Invalid email address: {task_dict['assigned_to']}")
    
    # Validate due date (if provided)
    if 'due_date' in task_dict and task_dict['due_date']:
        if not validate_date_format(task_dict['due_date']):
            errors.append(f"Invalid date format: {task_dict['due_date']}. Use YYYY-MM-DD")
    
    # Validate tags (if provided)
    if 'tags' in task_dict and task_dict['tags']:
        for tag in task_dict['tags']:
            if not validate_tag(tag):
                errors.append(f"Invalid tag format: {tag}")
    
    # Validate time (if provided)
    if 'time' in task_dict and task_dict['time']:
        if not validate_time_format(task_dict['time']):
            errors.append(f"Invalid time format: {task_dict['time']}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def sanitize_description(description: str) -> str:
    """
    Clean and sanitize a task description.
    
    Removes extra whitespace and trims the description.
    
    Args:
        description: Raw description string
        
    Returns:
        Cleaned description
        
    Example:
        >>> sanitize_description("  Buy   milk  ")
        'Buy milk'
    """
    if not description:
        return ""
    
    # Remove extra whitespace
    description = ' '.join(description.split())
    
    # Trim
    description = description.strip()
    
    return description