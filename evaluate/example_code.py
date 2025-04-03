"""Module docstring for example_code.py."""

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def subtract(a, b):
    """Return the difference of a and b."""
    return a - b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


def divide(a, b):
    """Return the quotient of a and b, raising ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def buggy_function(x):
    """Return result of division that intentionally causes a ZeroDivisionError."""
    return x / 0  # This will raise a ZeroDivisionError


def another_function(a, b):
    """Return the sum of a and b."""
    return a + b


def faulty_logic(a, b):
    """Return difference based on faulty logic that might be incorrect."""
    if a > b:
        return b - a  # This logic might be incorrect based on the intended functionality
    return a - b