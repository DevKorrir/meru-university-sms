import json
import os
from datetime import datetime

def save_to_json(data, filename):
    """Save data to JSON file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
        return False

def load_from_json(filename):
    """Load data from JSON file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading from {filename}: {e}")
        return None

def generate_id(prefix, existing_ids, length=4):
    """Generate a unique ID with given prefix"""
    if not existing_ids:
        return f"{prefix}1".zfill(len(prefix) + length)

    # Extract numeric parts and find max
    numbers = []
    for id_str in existing_ids:
        if id_str.startswith(prefix):
            try:
                num = int(id_str[len(prefix):])
                numbers.append(num)
            except ValueError:
                continue

    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{next_num}".zfill(len(prefix) + length)

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()

def format_currency(amount):
    """Format amount as currency"""
    return f"Ksh {amount:,.2f}"

def validate_input(prompt, validation_func, error_message="Invalid input"):
    """Get validated input from user"""
    while True:
        try:
            value = input(prompt)
            if validation_func(value):
                return value
            print(error_message)
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return None
        except Exception as e:
            print(f"Error: {e}")
