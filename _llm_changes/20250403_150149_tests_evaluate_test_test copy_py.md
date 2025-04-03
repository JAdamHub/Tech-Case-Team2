---
layout: llm_change
title: "Generated Tests for test copy.py"
date: 2025-04-03T15:01:49.900950
file: "tests/evaluate/test_test copy.py"
change_type: "Test Generation"
source_file: "evaluate/test copy.py"
consolidated: true
---
```python
import pytest
from evaluate.test_copy import (
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
    assert add_numbers(10, 15) == 25
    # Edge cases including 0 and negative numbers
    assert add_numbers(0, 0) == 0
    assert add_numbers(-5, 5) == 0
    # Floating point addition
    assert add_numbers(1.5, 2.5) == 4.0

def test_subtract_numbers():
    # Typical cases
    assert subtract_numbers(10, 5) == 5
    assert subtract_numbers(5, 10) == -5
    # Edge cases including 0 and negative numbers
    assert subtract_numbers(0, 0) == 0
    assert subtract_numbers(-10, -5) == -5

def test_multiply_numbers():
    # Typical cases
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-3, 4) == -12
    # Edge cases involving 0
    assert multiply_numbers(0, 100) == 0
    # Floating point multiplication
    assert multiply_numbers(2.5, 2) == 5.0

def test_divide_numbers():
    # Typical division
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(-10, 2) == -5
    # Floating point division
    assert divide_numbers(7, 2) == 3.5
    # Division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_concatenate_strings():
    # Typical string concatenation
    assert concatenate_strings("foo", "bar") == "foobar"
    # Concatenation with an empty string
    assert concatenate_strings("", "test") == "test"
    assert concatenate_strings("test", "") == "test"
    # Concatenation with spaces and punctuation
    assert concatenate_strings("hello ", "world!") == "hello world!"

def test_list_index_error():
    # This function should safely return an element from a list, avoiding an IndexError
    result = list_index_error()
    # According to the implementation, it returns the first element of [1, 2, 3]
    assert result == 1
```