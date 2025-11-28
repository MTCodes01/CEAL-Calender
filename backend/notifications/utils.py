import pytz
from datetime import datetime, time
from django.conf import settings


def convert_to_local(utc_time, timezone_str):
    """
    Convert UTC datetime to user's local timezone
    
    Args:
        utc_time: datetime object in UTC
        timezone_str: timezone string (e.g., 'Asia/Kolkata')
    
    Returns:
        datetime object in user's local timezone
    """
    try:
        user_tz = pytz.timezone(timezone_str)
        return utc_time.astimezone(user_tz)
    except Exception:
        # Fallback to UTC if timezone is invalid
        return utc_time


def is_within_minute(time1, time2):
    """
    Check if two time objects are within the same minute
    
    Args:
        time1: time object
        time2: time object
    
    Returns:
        bool: True if times are within the same minute
    """
    if not time1 or not time2:
        return False
    
    return time1.hour == time2.hour and time1.minute == time2.minute


def format_event_datetime(dt, timezone_str):
    """
    Format event datetime for display in user's timezone
    
    Args:
        dt: datetime object
        timezone_str: timezone string
    
    Returns:
        str: Formatted datetime string
    """
    try:
        user_tz = pytz.timezone(timezone_str)
        local_dt = dt.astimezone(user_tz)
        return local_dt.strftime('%B %d, %Y at %I:%M %p')
    except Exception:
        return dt.strftime('%B %d, %Y at %I:%M %p')
