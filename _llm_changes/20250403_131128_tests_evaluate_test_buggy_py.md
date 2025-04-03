---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T13:11:28.379117
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
    assert add_numbers(10, 15) == 25
    # Edge cases with zero and negative numbers
    assert add_numbers(0, 0) == 0
    assert add_numbers(-5, 10) == 5
    assert add_numbers(-3, -7) == -10


def test_subtract_numbers():
    # Typical cases
    assert subtract_numbers(10, 4) == 6
    assert subtract_numbers(4, 10) == -6
    # Edge cases with zero and negative numbers
    assert subtract_numbers(0, 0) == 0
    assert subtract_numbers(-5, -10) == 5
    assert subtract_numbers(0, 5) == -5


def test_multiply_numbers():
    # Typical cases
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-3, 4) == -12
    # Edge cases with zero and negative numbers
    assert multiply_numbers(0, 100) == 0
    assert multiply_numbers(-5, -5) == 25


def test_divide_numbers():
    # Typical cases
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(9, 2) == 4.5
    # Edge case: division by a negative number
    assert divide_numbers(10, -2) == -5
    # Error condition: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)


def test_concatenate_strings():
    # Typical cases
    assert concatenate_strings("Hello", "World") == "HelloWorld"
    # Edge cases with empty strings
    assert concatenate_strings("", "Test") == "Test"
    assert concatenate_strings("Test", "") == "Test"
    # Both empty strings
    assert concatenate_strings("", "") == ""
    # Concatenation of spaces and words
    assert concatenate_strings("Hello ", "World") == "Hello World"


def test_list_index_error():
    # The function should return the first element of the list [1, 2, 3]
    assert list_index_error() == 1
```