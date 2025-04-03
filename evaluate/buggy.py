"""Module for arithmetic and string operations with sample functions."""

def add_numbers(x, y):
    """Return the sum of x and y."""
    return x + y

def subtract_numbers(x, y):
    """Return the difference between x and y."""
    return x - y

def multiply_numbers(x, y):
    """Return the product of x and y."""
    return x * y

def divide_numbers(x, y):
    """Return the result of dividing x by y. Raises ZeroDivisionError if y is zero."""
    return x / y

def concatenate_strings(s1, s2):
    """Return the concatenation of s1 and s2."""
    return s1 + s2

def list_index_error():
    """Return a valid element from the list to avoid IndexError."""
    local_list = [1, 2, 3]
    return local_list[0]