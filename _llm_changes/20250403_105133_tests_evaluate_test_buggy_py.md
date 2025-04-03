---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for buggy.py"
date: 2025-04-03T10:51:33.044629
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

def test_add_numbers():
    # Typical cases:
    assert add_numbers(1, 2) == 3
    assert add_numbers(-5, -10) == -15
    # Edge case: adding zeros
    assert add_numbers(0, 0) == 0
    # Mixed types
    assert add_numbers(0, 7) == 7

def test_subtract_numbers():
    # Since subtract_numbers uses an undefined variable 'c', it should raise NameError.
    with pytest.raises(NameError):
        subtract_numbers(10, 5)

def test_multiply_numbers():
    # Typical multiplication
    assert multiply_numbers(3, 4) == 12
    # Edge cases:
    # Multiplication with zero
    assert multiply_numbers(0, 100) == 0
    # Multiplication with negative numbers
    assert multiply_numbers(-2, 3) == -6

def test_divide_numbers():
    # divide_numbers divides by zero always, so should raise ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 2)

def test_concatenate_strings():
    # Since concatenate_strings uses an undefined variable 's3', it should raise NameError.
    with pytest.raises(NameError):
        concatenate_strings("Hello", "World")

def test_list_index_error():
    # list_index_error will attempt to access an out-of-bound index in the list, raising IndexError.
    with pytest.raises(IndexError):
        list_index_error()
```