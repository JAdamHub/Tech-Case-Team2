---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for buggy.py"
date: 2025-04-03T11:15:31.797292
file: "tests/evaluate/test_buggy.py" # Report is about the test file
change_type: "Test Generation"
source_file: "evaluate/buggy.py"
---
```python
import pytest
from evaluate.buggy import add_numbers, subtract_numbers, multiply_numbers, divide_numbers, concatenate_strings, list_index_error

def test_add_numbers():
    # Typical numeric addition
    assert add_numbers(1, 2) == 3
    assert add_numbers(-5, 10) == 5
    assert add_numbers(2.5, 3.5) == 6.0
    
    # Edge case: string concatenation (works because '+' is overloaded for strings)
    # Note: This may not be the intended use of add_numbers, but the function supports it.
    assert add_numbers("Hello, ", "World") == "Hello, World"

def test_subtract_numbers():
    # subtract_numbers is buggy because it refers to an undefined variable 'c'
    with pytest.raises(NameError):
        subtract_numbers(10, 5)

def test_multiply_numbers():
    # Typical multiplication
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-2, 6) == -12
    # Edge case: one operand is zero
    assert multiply_numbers(0, 100) == 0

def test_divide_numbers():
    # divide_numbers is intentionally buggy: it tries to divide by zero regardless of input.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 2)

def test_concatenate_strings():
    # concatenate_strings is buggy because it refers to an undefined variable 's3'
    with pytest.raises(NameError):
        concatenate_strings("foo", "bar")

def test_list_index_error():
    # list_index_error will raise an IndexError due to an out-of-range list index.
    with pytest.raises(IndexError):
        list_index_error()
```