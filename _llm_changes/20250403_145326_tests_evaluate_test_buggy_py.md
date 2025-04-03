---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T14:53:26.108787
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
    # Typical case: positive integers
    assert add_numbers(2, 3) == 5
    # Typical case: negative numbers
    assert add_numbers(-2, -5) == -7
    # Mixed signs
    assert add_numbers(-3, 3) == 0
    # Floats
    assert add_numbers(2.5, 3.5) == 6.0

def test_subtract_numbers():
    # Typical case: positive integers
    assert subtract_numbers(5, 3) == 2
    # Negative result
    assert subtract_numbers(3, 5) == -2
    # Zero subtraction
    assert subtract_numbers(5, 0) == 5
    # Floats
    assert subtract_numbers(5.5, 2.2) == 3.3

def test_multiply_numbers():
    # Typical case: positive integers
    assert multiply_numbers(4, 5) == 20
    # Multiplying by zero
    assert multiply_numbers(4, 0) == 0
    # Negative numbers
    assert multiply_numbers(-3, 3) == -9
    # Floats
    assert multiply_numbers(2.5, 4) == 10.0

def test_divide_numbers():
    # Typical case: positive numbers
    assert divide_numbers(10, 2) == 5
    # Division resulting in float
    assert divide_numbers(3, 2) == 1.5
    # Negative division
    assert divide_numbers(-10, 2) == -5
    # Division by negative number
    assert divide_numbers(10, -2) == -5

    # Edge case: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_concatenate_strings():
    # Typical strings
    assert concatenate_strings("Hello", "World") == "HelloWorld"
    # With empty string
    assert concatenate_strings("", "World") == "World"
    assert concatenate_strings("Hello", "") == "Hello"
    # Both empty
    assert concatenate_strings("", "") == ""
    # Concatenation of longer strings
    s1 = "Python " * 3
    s2 = "Testing" * 2
    assert concatenate_strings(s1, s2) == s1 + s2

def test_list_index_error():
    # The function should always return the first element of the list [1, 2, 3], which is 1.
    assert list_index_error() == 1
```