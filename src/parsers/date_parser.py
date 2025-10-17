"""
Date parsing and conversion utilities.

This module handles conversion of various date formats including
relative dates like 'tomorrow', 'today', 'next week' to YYYY-MM-DD format.
"""

from datetime import datetime, timedelta
import re
from typing import Optional


def parse_date(date_string: str) -> Optional[str]:
    """
    Parse various date formats and return YYYY-MM-DD format.
    
    Handles:
    - YYYY-MM-DD format (returns as-is)
    - Relative dates (today, tomorrow, yesterday)
    - Next week, next month
    
    Args:
        date_string: Date string to parse
        
    Returns:
        Date in YYYY-MM-DD format, or None if invalid
        
    Example:
        >>> parse_date("2025-10-20")
        '2025-10-20'
        >>> parse_date("tomorrow")  # If today is 2025-10-17
        '2025-10-18'
    """
    if not date_string:
        return None
    
    date_string = date_string.lower().strip()
    
    # Check if already in YYYY-MM-DD format
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
        try:
            # Validate it's a real date
            datetime.strptime(date_string, '%Y-%m-%d')
            return date_string
        except ValueError:
            return None
    
    # Parse relative dates
    today = datetime.now().date()
    
    if date_string == 'today':
        return today.isoformat()
    
    elif date_string == 'tomorrow':
        return (today + timedelta(days=1)).isoformat()
    
    elif date_string == 'yesterday':
        return (today - timedelta(days=1)).isoformat()
    
    elif 'next week' in date_string:
        return (today + timedelta(weeks=1)).isoformat()
    
    elif 'next month' in date_string:
        # Approximate - add 30 days
        return (today + timedelta(days=30)).isoformat()
    
    elif date_string.endswith('days'):
        # Pattern like "3 days", "in 5 days"
        match = re.search(r'(\d+)\s*days?', date_string)
        if match:
            days = int(match.group(1))
            return (today + timedelta(days=days)).isoformat()
    
    elif date_string.endswith('weeks'):
        # Pattern like "2 weeks", "in 3 weeks"
        match = re.search(r'(\d+)\s*weeks?', date_string)
        if match:
            weeks = int(match.group(1))
            return (today + timedelta(weeks=weeks)).isoformat()
    
    # If nothing matched, return None
    return None


def parse_time(time_string: str) -> Optional[str]:
    """
    Parse time string and return in HH:MM format.
    
    Handles:
    - 24-hour format: "14:00", "9:30"
    - 12-hour format: "3pm", "11am", "3:30pm"
    
    Args:
        time_string: Time string to parse
        
    Returns:
        Time in HH:MM 24-hour format, or None if invalid
        
    Example:
        >>> parse_time("3pm")
        '15:00'
        >>> parse_time("14:00")
        '14:00'
    """
    if not time_string:
        return None
    
    time_string = time_string.lower().strip()
    
    # Already in HH:MM format
    if re.match(r'^\d{1,2}:\d{2}$', time_string):
        try:
            hour, minute = map(int, time_string.split(':'))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}"
        except ValueError:
            return None
    
    # 12-hour format with am/pm
    match = re.match(r'^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$', time_string)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        period = match.group(3)
        
        if not (1 <= hour <= 12 and 0 <= minute <= 59):
            return None
        
        # Convert to 24-hour format
        if period == 'pm' and hour != 12:
            hour += 12
        elif period == 'am' and hour == 12:
            hour = 0
        
        return f"{hour:02d}:{minute:02d}"
    
    return None


def get_relative_date_offset(date_string: str) -> Optional[int]:
    """
    Get the number of days offset for a relative date.
    
    Args:
        date_string: Relative date string
        
    Returns:
        Number of days from today, or None if not a relative date
        
    Example:
        >>> get_relative_date_offset("tomorrow")
        1
        >>> get_relative_date_offset("yesterday")
        -1
    """
    date_string = date_string.lower().strip()
    
    if date_string == 'today':
        return 0
    elif date_string == 'tomorrow':
        return 1
    elif date_string == 'yesterday':
        return -1
    elif 'next week' in date_string:
        return 7
    elif 'next month' in date_string:
        return 30
    
    # Pattern like "3 days"
    match = re.search(r'(\d+)\s*days?', date_string)
    if match:
        return int(match.group(1))
    
    # Pattern like "2 weeks"
    match = re.search(r'(\d+)\s*weeks?', date_string)
    if match:
        return int(match.group(1)) * 7
    
    return None


def is_valid_date_range(start_date: str, end_date: str) -> bool:
    """
    Check if a date range is valid (start before end).
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        
    Returns:
        True if start_date is before or equal to end_date
        
    Example:
        >>> is_valid_date_range("2025-10-01", "2025-10-31")
        True
        >>> is_valid_date_range("2025-10-31", "2025-10-01")
        False
    """
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        return start <= end
    except ValueError:
        return False