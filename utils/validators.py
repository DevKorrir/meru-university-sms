import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_year(year):
    """Validate student year (1-5)"""
    return isinstance(year, int) and 1 <= year <= 5

def validate_capacity(capacity):
    """Validate course capacity"""
    return isinstance(capacity, int) and capacity > 0

def validate_isbn(isbn):
    """Validate ISBN format (simplified)"""
    if not isbn or not isinstance(isbn, str):
        return False
    # Simple ISBN validation - can be enhanced
    return len(isbn) >= 10 and isbn.replace('-', '').isalnum()

def validate_amount(amount):
    """Validate payment amount"""
    return isinstance(amount, (int, float)) and amount >= 0

def validate_date(date_str):
    """Validate date string (YYYY-MM-DD)"""
    if not date_str or not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_student_id(student_id):
    """Validate student ID format"""
    if not student_id or not isinstance(student_id, str):
        return False
    return student_id.startswith('S') and student_id[1:].isdigit()

def validate_course_id(course_id):
    """Validate course ID format"""
    if not course_id or not isinstance(course_id, str):
        return False
    return len(course_id) >= 2 and course_id.isalnum()
