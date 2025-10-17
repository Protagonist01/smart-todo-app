"""
Regular expression patterns for parsing task components.

This module contains all regex patterns used to extract information
from natural language task input strings.
"""

import re

# Matches tags like @shopping, @work, @personal
# Example: "@shopping" -> captures "shopping"
TAG_PATTERN = r'\s@(\w+)'


# Matches priority levels: #high, #medium, #low
# Example: "#high" -> captures "high"
PRIORITY_PATTERN = r'#(high|medium|low)'


# Matches due dates in format: due:YYYY-MM-DD
# Example: "due:2025-10-20" -> captures "2025-10-20"
DUE_DATE_PATTERN = r'due:(\d{4}-\d{2}-\d{2})'

# Matches relative dates like "tomorrow", "today", "next week"
# Example: "due:tomorrow" -> captures "tomorrow"
RELATIVE_DATE_PATTERN = r'due:(today|tomorrow|yesterday|next\s+week|next\s+month)'


# Matches email addresses: assigned:user@example.com
# Example: "assigned:alice@example.com" -> captures "alice@example.com"
EMAIL_PATTERN = r'assigned:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'


# Matches time expressions like "at 3pm", "by 5:30 PM", "at 14:00"
# Example: "at 3pm" -> captures groups for hour, minutes, am/pm
TIME_PATTERN = r'(?:at|by)\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm|AM|PM)?'


# Matches duration like "1h", "30m", "2h30m"
# Example: "1h30m" -> captures "1h30m"
DURATION_PATTERN =  r'\b\d+h\d*m?\b|\b\d+m\b'


# Pre-compile patterns for faster matching
COMPILED_TAG = re.compile(TAG_PATTERN, re.IGNORECASE)
COMPILED_PRIORITY = re.compile(PRIORITY_PATTERN, re.IGNORECASE)
COMPILED_DUE_DATE = re.compile(DUE_DATE_PATTERN)
COMPILED_RELATIVE_DATE = re.compile(RELATIVE_DATE_PATTERN, re.IGNORECASE)
COMPILED_EMAIL = re.compile(EMAIL_PATTERN, re.IGNORECASE)
COMPILED_TIME = re.compile(TIME_PATTERN, re.IGNORECASE)
COMPILED_DURATION = re.compile(DURATION_PATTERN)



PATTERNS = {
    'tag': COMPILED_TAG,
    'priority': COMPILED_PRIORITY,
    'due_date': COMPILED_DUE_DATE,
    'relative_date': COMPILED_RELATIVE_DATE,
    'email': COMPILED_EMAIL,
    'time': COMPILED_TIME,
    'duration': COMPILED_DURATION,
}


def get_pattern(pattern_name: str):
    """
    Get a compiled regex pattern by name.
    
    Args:
        pattern_name: Name of the pattern to retrieve
        
    Returns:
        Compiled regex pattern or None if not found
        
    Example:
        >>> tag_pattern = get_pattern('tag')
        >>> tag_pattern.findall("Buy milk @shopping @urgent")
        ['shopping', 'urgent']
    """
    return PATTERNS.get(pattern_name)