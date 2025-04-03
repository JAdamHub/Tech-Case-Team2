---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T14:46:34.737513
file: "tests/evaluate/test_buggy.py"
change_type: "Test Generation"
source_file: "evaluate/buggy.py"
consolidated: true
---
```python
import pytest
from evaluate.buggy import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
    concatenate_strings,
    list_index_error
)

def test_add_numbers():
    # Typical cases
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, -2) == -3
    assert add_numbers(0, 5) == 5
    # Floats
    assert add_numbers(2.5, 3.5) == 6.0
    # Edge Case: adding zero
    assert add_numbers(0, 0) == 0

def test_subtract_numbers():
    # Typical cases
    assert subtract_numbers(5, 3) == 2
    assert subtract_numbers(3, 5) == -2
    # Negative numbers
    assert subtract_numbers(-5, -3) == -2
    # Edge Case: subtracting zero
    assert subtract_numbers(5, 0) == 5
    assert subtract_numbers(0, 5) == -5

def test_multiply_numbers():
    # Typical cases
    assert multiply_numbers(2, 3) == 6
    assert multiply_numbers(-2, 3) == -6
    assert multiply_numbers(-2, -3) == 6
    # Edge Case: multiplication by zero
    assert multiply_numbers(0, 10) == 0
    assert multiply_numbers(10, 0) == 0

def test_divide_numbers():
    # Typical division
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(3, 2) == 1.5
    # Negative division
    assert divide_numbers(-10, 2) == -5
    # Edge case: division resulting in float
    assert divide_numbers(0, 5) == 0.0

    # Error condition: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_concatenate_strings():
    # Typical cases
    assert concatenate_strings("hello", "world") == "helloworld"
    # Edge cases: empty strings
    assert concatenate_strings("", "world") == "world"
    assert concatenate_strings("hello", "") == "hello"
    # Concatenating two empty strings
    assert concatenate_strings("", "") == ""
    # Concatenation with spaces
    assert concatenate_strings("hello ", "world") == "hello world"

def test_list_index_error():
    # The function should return the first element of the list [1, 2, 3]
    assert list_index_error() == 1
```