---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for buggy.py"
date: 2025-04-03T11:22:22.595800
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
    # Typical case: integers
    assert add_numbers(1, 2) == 3
    # Typical case: floats
    assert add_numbers(1.5, 2.5) == 4.0
    # Edge case: negative numbers
    assert add_numbers(-5, -10) == -15
    # Edge case: mixing positive and negative
    assert add_numbers(-10, 20) == 10
    # Edge case: zeros
    assert add_numbers(0, 0) == 0

def test_subtract_numbers():
    # Since subtract_numbers uses an undefined variable 'c',
    # it should raise a NameError. We'll test that error is raised.
    with pytest.raises(NameError):
        subtract_numbers(5, 3)

def test_multiply_numbers():
    # Typical case: integers
    assert multiply_numbers(3, 4) == 12
    # Typical case: one number is zero
    assert multiply_numbers(0, 10) == 0
    # Edge case: negative numbers
    assert multiply_numbers(-2, 5) == -10
    # Typical case: floats
    assert multiply_numbers(2.5, 4) == 10.0

def test_divide_numbers():
    # Since divide_numbers divides by zero regardless of inputs,
    # it should raise a ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 5)
    with pytest.raises(ZeroDivisionError):
        divide_numbers(-3, 9)

def test_concatenate_strings():
    # Since concatenate_strings uses an undefined variable 's3',
    # it should raise a NameError.
    with pytest.raises(NameError):
        concatenate_strings("hello", "world")

def test_list_index_error():
    # list_index_error should raise an IndexError because
    # it tries to access an index that doesn't exist.
    with pytest.raises(IndexError):
        list_index_error()
```