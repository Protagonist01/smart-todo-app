"""
Unit tests for date parser module.
"""

import pytest
from datetime import datetime, timedelta
from src.parsers.date_parser import (
    parse_date,
    parse_time,
    get_relative_date_offset,
    is_valid_date_range
)


class TestParseDate:
    """Tests for date parsing."""
    
    def test_parse_exact_date(self):
        """Test parsing exact date format."""
        assert parse_date("2025-10-20") == "2025-10-20"
        assert parse_date("2025-01-01") == "2025-01-01"
    
    def test_parse_today(self):
        """Test parsing 'today'."""
        today = datetime.now().date().isoformat()
        assert parse_date("today") == today
        assert parse_date("TODAY") == today  # Case insensitive
    
    def test_parse_tomorrow(self):
        """Test parsing 'tomorrow'."""
        tomorrow = (datetime.now().date() + timedelta(days=1)).isoformat()
        assert parse_date("tomorrow") == tomorrow
        assert parse_date("TOMORROW") == tomorrow
    
    def test_parse_yesterday(self):
        """Test parsing 'yesterday'."""
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        assert parse_date("yesterday") == yesterday
    
    def test_parse_next_week(self):
        """Test parsing 'next week'."""
        next_week = (datetime.now().date() + timedelta(weeks=1)).isoformat()
        assert parse_date("next week") == next_week
    
    def test_parse_next_month(self):
        """Test parsing 'next month'."""
        next_month = (datetime.now().date() + timedelta(days=30)).isoformat()
        assert parse_date("next month") == next_month
    
    def test_parse_days_offset(self):
        """Test parsing '3 days', 'in 5 days'."""
        three_days = (datetime.now().date() + timedelta(days=3)).isoformat()
        assert parse_date("3 days") == three_days
        assert parse_date("in 5 days") == (datetime.now().date() + timedelta(days=5)).isoformat()
    
    def test_parse_weeks_offset(self):
        """Test parsing '2 weeks', 'in 3 weeks'."""
        two_weeks = (datetime.now().date() + timedelta(weeks=2)).isoformat()
        assert parse_date("2 weeks") == two_weeks
    
    def test_parse_invalid_date(self):
        """Test parsing invalid date."""
        assert parse_date("invalid") is None
        assert parse_date("2025-13-01") is None  # Invalid month
        assert parse_date("") is None
        assert parse_date(None) is None
    
    def test_parse_with_whitespace(self):
        """Test parsing with extra whitespace."""
        assert parse_date("  today  ") == datetime.now().date().isoformat()
        assert parse_date("  2025-10-20  ") == "2025-10-20"


class TestParseTime:
    """Tests for time parsing."""
    
    def test_parse_24_hour_format(self):
        """Test parsing 24-hour format."""
        assert parse_time("14:00") == "14:00"
        assert parse_time("09:30") == "09:30"
        assert parse_time("0:00") == "00:00"
        assert parse_time("23:59") == "23:59"
    
    def test_parse_12_hour_format_pm(self):
        """Test parsing 12-hour format with PM."""
        assert parse_time("3pm") == "15:00"
        assert parse_time("12pm") == "12:00"
        assert parse_time("11pm") == "23:00"
        assert parse_time("3:30pm") == "15:30"
    
    def test_parse_12_hour_format_am(self):
        """Test parsing 12-hour format with AM."""
        assert parse_time("3am") == "03:00"
        assert parse_time("12am") == "00:00"
        assert parse_time("9:30am") == "09:30"
    
    def test_parse_case_insensitive(self):
        """Test parsing is case insensitive."""
        assert parse_time("3PM") == "15:00"
        assert parse_time("3Am") == "03:00"
    
    def test_parse_invalid_time(self):
        """Test parsing invalid time."""
        assert parse_time("25:00") is None  # Invalid hour
        assert parse_time("12:60") is None  # Invalid minute
        assert parse_time("13pm") is None   # Invalid hour for PM
        assert parse_time("invalid") is None
        assert parse_time("") is None
    
    def test_parse_with_whitespace(self):
        """Test parsing with whitespace."""
        assert parse_time("  3pm  ") == "15:00"
        assert parse_time("  14:00  ") == "14:00"


class TestGetRelativeDateOffset:
    """Tests for relative date offset."""
    
    def test_today_offset(self):
        """Test 'today' offset."""
        assert get_relative_date_offset("today") == 0
    
    def test_tomorrow_offset(self):
        """Test 'tomorrow' offset."""
        assert get_relative_date_offset("tomorrow") == 1
    
    def test_yesterday_offset(self):
        """Test 'yesterday' offset."""
        assert get_relative_date_offset("yesterday") == -1
    
    def test_next_week_offset(self):
        """Test 'next week' offset."""
        assert get_relative_date_offset("next week") == 7
    
    def test_next_month_offset(self):
        """Test 'next month' offset."""
        assert get_relative_date_offset("next month") == 30
    
    def test_days_offset(self):
        """Test 'X days' offset."""
        assert get_relative_date_offset("3 days") == 3
        assert get_relative_date_offset("7 days") == 7
    
    def test_weeks_offset(self):
        """Test 'X weeks' offset."""
        assert get_relative_date_offset("2 weeks") == 14
        assert get_relative_date_offset("3 weeks") == 21
    
    def test_invalid_offset(self):
        """Test invalid relative date."""
        assert get_relative_date_offset("invalid") is None
        assert get_relative_date_offset("2025-10-20") is None


class TestIsValidDateRange:
    """Tests for date range validation."""
    
    def test_valid_date_range(self):
        """Test valid date range."""
        assert is_valid_date_range("2025-10-01", "2025-10-31") is True
        assert is_valid_date_range("2025-10-20", "2025-10-20") is True  # Same day
    
    def test_invalid_date_range(self):
        """Test invalid date range (end before start)."""
        assert is_valid_date_range("2025-10-31", "2025-10-01") is False
    
    def test_invalid_date_format(self):
        """Test with invalid date format."""
        assert is_valid_date_range("invalid", "2025-10-31") is False
        assert is_valid_date_range("2025-10-01", "invalid") is False