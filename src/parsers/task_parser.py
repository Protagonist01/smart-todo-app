"""
Task parser for extracting task components from natural language input.

This module uses regex patterns to extract tags, priority, due dates,
emails, and other metadata from task description strings.
"""

import re
from typing import Dict, Optional
from src.parsers.regex_patterns import (
    COMPILED_TAG,
    COMPILED_PRIORITY,
    COMPILED_DUE_DATE,
    COMPILED_RELATIVE_DATE,
    COMPILED_EMAIL,
    COMPILED_TIME,
    COMPILED_DURATION
)
from src.parsers.date_parser import parse_date, parse_time
from src.parsers.validator import validate_task_data, sanitize_description, validate_email, validate_priority
from src.models.task import Task


def extract_tags(text: str) -> list:
    """
    Extract all tags from text.
    
    Args:
        text: Input text containing tags
        
    Returns:
        List of extracted tags (without @ symbol)
        
    Example:
        >>> extract_tags("Buy milk @shopping @urgent")
        ['shopping', 'urgent']
    """
    matches = COMPILED_TAG.findall(text)
    return [tag.lower() for tag in matches]


def extract_priority(text: str) -> Optional[str]:
    """
    Extract priority level from text.
    
    Args:
        text: Input text containing priority
        
    Returns:
        Priority level (high/medium/low) or None
        
    Example:
        >>> extract_priority("Complete report #high")
        'high'
    """
    match = COMPILED_PRIORITY.search(text)
    if match:
        return match.group(1).lower()
    return None


def extract_due_date(text: str) -> Optional[str]:
    """
    Extract and parse due date from text.
    
    Args:
        text: Input text containing due date
        
    Returns:
        Due date in YYYY-MM-DD format or None
        
    Example:
        >>> extract_due_date("Submit report due:2025-10-20")
        '2025-10-20'
        >>> extract_due_date("Call client due:tomorrow")
        '2025-10-18'  # If today is 2025-10-17
    """
    # Try exact date format first
    match = COMPILED_DUE_DATE.search(text)
    if match:
        return match.group(1)
    
    # Try relative date
    match = COMPILED_RELATIVE_DATE.search(text)
    if match:
        relative_date = match.group(1)
        return parse_date(relative_date)
    
    return None


def extract_email(text: str) -> Optional[str]:
    """
    Extract assigned email address from text.
    
    Args:
        text: Input text containing email
        
    Returns:
        Email address or None
        
    Example:
        >>> extract_email("Review code assigned:alice@example.com")
        'alice@example.com'
    """
    match = COMPILED_EMAIL.search(text)
    if match:
        return match.group(1).lower()
    return None


def extract_time(text: str) -> Optional[str]:
    """
    Extract and parse time from text.
    
    Args:
        text: Input text containing time
        
    Returns:
        Time in HH:MM format or None
        
    Example:
        >>> extract_time("Meeting at 3pm")
        '15:00'
        >>> extract_time("Call by 9:30am")
        '09:30'
    """
    match = COMPILED_TIME.search(text)
    if match:
        hour = match.group(1)
        minute = match.group(2) or "00"
        period = match.group(3) or ""
        
        time_str = f"{hour}:{minute}{period}"
        return parse_time(time_str)
    
    return None


def extract_duration(text: str) -> Optional[str]:
    """
    Extract duration from text.
    """
    match = COMPILED_DURATION.search(text)
    if match:
        # match.group(0) contains the full match ("1h30m", "2h", etc.)
        return match.group(0)
    return None


def remove_metadata(text: str) -> str:
    """
    Remove all metadata (tags, priority, dates, etc.) from text.
    
    Leaves only the core task description.
    
    Args:
        text: Input text with metadata
        
    Returns:
        Clean task description
        
    Example:
        >>> remove_metadata("Buy milk @shopping #high due:2025-10-20")
        'Buy milk'
    """
    # Remove tags
    text = COMPILED_TAG.sub('', text)
    
    # Remove priority
    text = COMPILED_PRIORITY.sub('', text)
    
    # Remove due dates (both formats)
    text = COMPILED_DUE_DATE.sub('', text)
    text = COMPILED_RELATIVE_DATE.sub('', text)
    
    # Remove email
    text = COMPILED_EMAIL.sub('', text)
    
    # Remove time
    text = COMPILED_TIME.sub('', text)
    
    # Remove duration
    text = COMPILED_DURATION.sub('', text)
    
    # Clean up extra whitespace
    text = sanitize_description(text)
    
    return text


def parse_task_string(task_string: str) -> Dict[str, any]:
    """
    Parse a task string and extract all components into a dictionary.
    """

    if not task_string or not task_string.strip():
        raise ValueError("Task string cannot be empty")

    # Extract components
    tags = extract_tags(task_string)
    priority = extract_priority(task_string)
    due_date = extract_due_date(task_string)
    assigned_to = extract_email(task_string)
    time = extract_time(task_string)
    duration = extract_duration(task_string)

    # Remove metadata to isolate the description
    description = remove_metadata(task_string).strip()

    # --- Validation Section ---
    if not description:
        # pytest expects "description" in message
        raise ValueError("Invalid task: description is missing")

    if priority and not validate_priority(priority):
        # pytest expects "priority" in message
        raise ValueError(f"Invalid priority: {priority}")

    if assigned_to and not validate_email(assigned_to):
        # pytest expects "email" in message
        raise ValueError(f"Invalid email: {assigned_to}")

    # Build the task data
    task_data = {
        "description": description,
        "tags": tags,
        "priority": priority,
        "due_date": due_date,
        "assigned_to": assigned_to,
        "time": time,
        "duration": duration,
    }

    # Validate overall data consistency
    is_valid, errors = validate_task_data(task_data)
    if not is_valid and errors:
        raise ValueError(" | ".join(errors))

    return task_data



def create_task_from_string(task_string: str) -> Task:
    """
    Parse a task string and create a Task object.
    
    This is the high-level function that combines parsing and Task creation.
    
    Args:
        task_string: Raw task input string
        
    Returns:
        New Task instance
        
    Raises:
        ValueError: If task string is invalid
        
    Example:
        >>> task = create_task_from_string(
        ...     "Buy groceries @shopping #high due:2025-10-20"
        ... )
        >>> task.description
        'Buy groceries'
        >>> task.priority
        'high'
    """
    # Parse the string
    task_data = parse_task_string(task_string)
    
    # Create and return Task object
    # Remove None values to use Task defaults
    task_data = {k: v for k, v in task_data.items() if v is not None}
    
    return Task(**task_data)


def parse_multiple_tasks(task_strings: list) -> list:
    """
    Parse multiple task strings and return list of Task objects.
    
    Args:
        task_strings: List of task input strings
        
    Returns:
        List of Task objects
        
    Example:
        >>> tasks = parse_multiple_tasks([
        ...     "Buy milk @shopping",
        ...     "Review code @work #high"
        ... ])
        >>> len(tasks)
        2
    """
    tasks = []
    errors = []
    
    for i, task_string in enumerate(task_strings):
        try:
            task = create_task_from_string(task_string)
            tasks.append(task)
        except ValueError as e:
            errors.append(f"Line {i+1}: {str(e)}")
    
    if errors:
        print("Some tasks failed to parse:")
        for error in errors:
            print(f"  {error}")
    
    return tasks