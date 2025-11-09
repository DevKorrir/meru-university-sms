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
        return f"{prefix}{str(1).zfill(length)}"

    # Extract numeric parts and find max
    numbers = []
    for id_str in existing_ids:
        # Check if ID contains the prefix (handle zero-padded IDs)
        if prefix in id_str:
            try:
                # Extract the numeric part after the prefix
                num_part = id_str.split(prefix)[-1]
                num = int(num_part)
                numbers.append(num)
            except ValueError:
                continue

    next_num = max(numbers) + 1 if numbers else 1
    return f"{prefix}{str(next_num).zfill(length)}"

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
