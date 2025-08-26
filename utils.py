"""
Utility Functions Module
========================

This module contains utility functions for input validation, formatting,
and common operations used throughout the application.

Key Concepts Demonstrated:
- Function definition and parameters
- Input validation and error handling
- Regular expressions
- String manipulation
- Type hints and documentation
- Exception handling
"""

import os
import re
import sys
from typing import Union, Optional


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str):
    """
    Print a formatted header with the given title.
    
    Args:
        title (str): The title to display
    """
    print("=" * 60)
    print(f"{title:^60}")
    print("=" * 60)


def print_separator():
    """Print a separator line."""
    print("-" * 60)


def get_valid_input(prompt: str, input_type: str = "str", min_val: Optional[Union[int, float]] = None, 
                   max_val: Optional[Union[int, float]] = None, min_length: Optional[int] = None, 
                   max_length: Optional[int] = None, required: bool = True) -> Union[str, int, float]:
    """
    Get validated input from the user with comprehensive error checking.
    
    Args:
        prompt (str): The prompt to display to the user
        input_type (str): Type of input expected ("str", "int", "float", "email")
        min_val (Optional[Union[int, float]]): Minimum value for numeric inputs
        max_val (Optional[Union[int, float]]): Maximum value for numeric inputs
        min_length (Optional[int]): Minimum length for string inputs
        max_length (Optional[int]): Maximum length for string inputs
        required (bool): Whether input is required (default: True)
    
    Returns:
        Union[str, int, float]: Validated input value
    
    Raises:
        KeyboardInterrupt: If user presses Ctrl+C
    """
    while True:
        try:
            user_input = input(prompt).strip()
            
            # Handle empty input
            if not user_input:
                if not required:
                    return ""
                print("❌ Input cannot be empty. Please try again.")
                continue
            
            # Validate based on input type
            if input_type == "str":
                if min_length is not None and len(user_input) < min_length:
                    print(f"❌ Input must be at least {min_length} characters long.")
                    continue
                
                if max_length is not None and len(user_input) > max_length:
                    print(f"❌ Input must be no more than {max_length} characters long.")
                    continue
                
                return user_input
            
            elif input_type == "int":
                try:
                    value = int(user_input)
                    
                    if min_val is not None and value < min_val:
                        print(f"❌ Value must be at least {min_val}.")
                        continue
                    
                    if max_val is not None and value > max_val:
                        print(f"❌ Value must be no more than {max_val}.")
                        continue
                    
                    return value
                
                except ValueError:
                    print("❌ Please enter a valid integer.")
                    continue
            
            elif input_type == "float":
                try:
                    value = float(user_input)
                    
                    if min_val is not None and value < min_val:
                        print(f"❌ Value must be at least {min_val}.")
                        continue
                    
                    if max_val is not None and value > max_val:
                        print(f"❌ Value must be no more than {max_val}.")
                        continue
                    
                    return value
                
                except ValueError:
                    print("❌ Please enter a valid number.")
                    continue
            
            elif input_type == "email":
                if is_valid_email(user_input):
                    return user_input.lower()
                else:
                    print("❌ Please enter a valid email address.")
                    continue
            
            else:
                raise ValueError(f"Unsupported input type: {input_type}")
        
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user.")
            raise


def is_valid_email(email: str) -> bool:
    """
    Validate email address format using regular expressions.
    
    Args:
        email (str): Email address to validate
    
    Returns:
        bool: True if email is valid, False otherwise
    """
    # Basic email validation regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def format_grade(grade: float) -> str:
    """
    Format a grade value for display.
    
    Args:
        grade (float): Grade value to format
    
    Returns:
        str: Formatted grade string
    """
    return f"{grade:.1f}%"


def format_percentage(value: float, total: float) -> str:
    """
    Calculate and format a percentage.
    
    Args:
        value (float): The value
        total (float): The total value
    
    Returns:
        str: Formatted percentage string
    """
    if total == 0:
        return "0.0%"
    
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"


def get_letter_grade_color(letter_grade: str) -> str:
    """
    Get a color code for a letter grade (for terminal display).
    
    Args:
        letter_grade (str): Letter grade (A, B, C, D, F)
    
    Returns:
        str: ANSI color code
    """
    colors = {
        'A': '\033[92m',  # Green
        'B': '\033[94m',  # Blue
        'C': '\033[93m',  # Yellow
        'D': '\033[91m',  # Red
        'F': '\033[95m'   # Magenta
    }
    return colors.get(letter_grade.upper(), '\033[0m')  # Default to reset


def format_colored_grade(letter_grade: str) -> str:
    """
    Format a letter grade with color for terminal display.
    
    Args:
        letter_grade (str): Letter grade to format
    
    Returns:
        str: Colored letter grade string
    """
    color = get_letter_grade_color(letter_grade)
    reset = '\033[0m'
    return f"{color}{letter_grade}{reset}"


def validate_student_id(student_id: str) -> bool:
    """
    Validate student ID format.
    
    Args:
        student_id (str): Student ID to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Student ID should be alphanumeric and 3-20 characters
    if not student_id or len(student_id) < 3 or len(student_id) > 20:
        return False
    
    return student_id.replace('-', '').replace('_', '').isalnum()


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename (str): Original filename
    
    Returns:
        str: Sanitized filename
    """
    # Remove invalid characters for filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "untitled"
    
    return filename


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length with an optional suffix.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
        suffix (str): Suffix to add if truncated (default: "...")
    
    Returns:
        str: Truncated string
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
    
    Returns:
        str: Formatted file size
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def confirm_action(message: str, default: bool = False) -> bool:
    """
    Ask user for confirmation of an action.
    
    Args:
        message (str): Confirmation message
        default (bool): Default response if user just presses Enter
    
    Returns:
        bool: True if user confirms, False otherwise
    """
    default_text = "Y/n" if default else "y/N"
    prompt = f"{message} [{default_text}]: "
    
    while True:
        try:
            response = input(prompt).strip().lower()
            
            if not response:
                return default
            
            if response in ['y', 'yes', 'true', '1']:
                return True
            elif response in ['n', 'no', 'false', '0']:
                return False
            else:
                print("❌ Please enter 'y' for yes or 'n' for no.")
        
        except KeyboardInterrupt:
            print("\n👋 Operation cancelled.")
            return False


def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', 
                      decimals: int = 1, length: int = 50, fill: str = '█') -> None:
    """
    Print a progress bar to the terminal.
    
    Args:
        iteration (int): Current iteration
        total (int): Total iterations
        prefix (str): Prefix string
        suffix (str): Suffix string
        decimals (int): Number of decimals in percent complete
        length (int): Character length of bar
        fill (str): Bar fill character
    """
    if total == 0:
        return
    
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='', flush=True)
    
    # Print newline on complete
    if iteration == total:
        print()


def create_backup_filename(original_filename: str) -> str:
    """
    Create a backup filename with timestamp.
    
    Args:
        original_filename (str): Original filename
    
    Returns:
        str: Backup filename with timestamp
    """
    from datetime import datetime
    
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    return f"{name}_backup_{timestamp}{ext}"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Args:
        numerator (float): Numerator
        denominator (float): Denominator
        default (float): Default value if division by zero
    
    Returns:
        float: Result of division or default value
    """
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default