---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T11:45:20.898120
file: "tests/evaluate/test_buggy.py"
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

def test_add_numbers():
    # Typical cases
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, -2) == -3
    # Edge cases
    assert add_numbers(0, 0) == 0
    # Floating point numbers
    assert add_numbers(1.5, 2.5) == 4.0

def test_subtract_numbers():
    # Typical cases
    assert subtract_numbers(5, 3) == 2
    assert subtract_numbers(3, 5) == -2
    # Edge cases
    assert subtract_numbers(0, 0) == 0
    # Floating point numbers
    assert subtract_numbers(2.5, 1.5) == 1.0

def test_multiply_numbers():
    # Typical cases
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-2, 4) == -8
    # Edge cases with zero
    assert multiply_numbers(0, 10) == 0
    # Floating point numbers
    assert multiply_numbers(1.2, 3.0) == 3.6

def test_divide_numbers():
    # Typical cases
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(-9, 3) == -3
    # Floating point division
    assert divide_numbers(5.0, 2.0) == 2.5
    # Error condition: Division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_concatenate_strings():
    # Typical cases
    assert concatenate_strings("Hello, ", "World!") == "Hello, World!"
    # Edge cases with empty strings
    assert concatenate_strings("", "Test") == "Test"
    assert concatenate_strings("Test", "") == "Test"
    assert concatenate_strings("", "") == ""
    # Single character strings
    assert concatenate_strings("a", "b") == "ab"

def test_list_index_error():
    # The function is expected to return the first element of the list [1, 2, 3]
    result = list_index_error()
    assert result == 1
```