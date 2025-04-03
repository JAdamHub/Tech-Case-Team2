---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for buggy.py"
date: 2025-04-03T10:57:41.434503
file: "tests/evaluate/test_buggy.py" # Report is about the test file
change_type: "Test Generation"
source_file: "evaluate/buggy.py"
---
```python
import pytest
from evaluate.buggy import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
    concatenate_strings,
    list_index_error,
)

# Test for add_numbers(a, b)
def test_add_numbers():
    # Typical case with integers
    assert add_numbers(2, 3) == 5
    # Edge case: adding zeros
    assert add_numbers(0, 0) == 0
    # Typical case with floats
    assert add_numbers(2.5, 3.5) == 6.0
    # Test with negative numbers
    assert add_numbers(-1, -2) == -3
    # Optionally, test string addition (which is allowed in Python)
    assert add_numbers("Hello ", "World") == "Hello World"

# Test for subtract_numbers(a, b)
def test_subtract_numbers():
    # Regardless of inputs, subtract_numbers is expected to raise a NameError because 'c' is undefined.
    with pytest.raises(NameError):
        subtract_numbers(5, 3)
    # Test with other typical values to ensure error consistently occurs.
    with pytest.raises(NameError):
        subtract_numbers(10, 4)

# Test for multiply_numbers(a, b)
def test_multiply_numbers():
    # Typical case with integers
    assert multiply_numbers(4, 5) == 20
    # Edge case with zero: multiplication by zero
    assert multiply_numbers(0, 100) == 0
    # Test with negative values
    assert multiply_numbers(-3, 6) == -18
    # Test with floats
    assert multiply_numbers(2.5, 4) == 10.0

# Test for divide_numbers(a, b)
def test_divide_numbers():
    # Since the function always divides by 0, it should always raise a ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 2)
    with pytest.raises(ZeroDivisionError):
        divide_numbers(100, 5)

# Test for concatenate_strings(s1, s2)
def test_concatenate_strings():
    # Even with valid string inputs, the function references an undefined variable (s3) and should raise a NameError.
    with pytest.raises(NameError):
        concatenate_strings("Hello", "World")
    with pytest.raises(NameError):
        concatenate_strings("", "")

# Test for list_index_error()
def test_list_index_error():
    # The function attempts to access an out-of-bound index and should raise an IndexError.
    with pytest.raises(IndexError):
        list_index_error()
```