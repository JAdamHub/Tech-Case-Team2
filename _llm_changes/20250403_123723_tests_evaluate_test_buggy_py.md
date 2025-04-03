---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T12:37:23.404811
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
    list_index_error,
)


def test_add_numbers():
    # Test with positive integers
    assert add_numbers(2, 3) == 5
    # Test with negative integers
    assert add_numbers(-1, -1) == -2
    # Test with a mix of positive and negative
    assert add_numbers(-5, 10) == 5
    # Test with floats
    assert add_numbers(2.5, 3.5) == 6.0
    # Test with zeros
    assert add_numbers(0, 0) == 0


def test_subtract_numbers():
    # Test with positive integers
    assert subtract_numbers(10, 5) == 5
    # Test with negative integers
    assert subtract_numbers(-5, -10) == 5
    # Test with a mix of positive and negative
    assert subtract_numbers(5, -5) == 10
    # Test with floats
    assert subtract_numbers(5.5, 2.5) == 3.0
    # Test with zeros
    assert subtract_numbers(0, 0) == 0


def test_multiply_numbers():
    # Test with positive integers
    assert multiply_numbers(3, 4) == 12
    # Test with negative integers
    assert multiply_numbers(-2, 3) == -6
    # Test with a mix of positive and negative
    assert multiply_numbers(-3, -4) == 12
    # Test with zero multiplication
    assert multiply_numbers(0, 100) == 0
    # Test with floats
    assert multiply_numbers(2.5, 4) == 10.0


def test_divide_numbers():
    # Test with positive integers
    assert divide_numbers(10, 2) == 5.0
    # Test with non-integer division
    assert divide_numbers(7, 2) == 3.5
    # Test with negative values
    assert divide_numbers(-10, 2) == -5.0
    # Test with division where numerator is negative
    assert divide_numbers(10, -2) == -5.0
    # Test that division by zero raises a ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(5, 0)


def test_concatenate_strings():
    # Test with non-empty strings
    assert concatenate_strings("foo", "bar") == "foobar"
    # Test with an empty first string
    assert concatenate_strings("", "test") == "test"
    # Test with an empty second string
    assert concatenate_strings("hello", "") == "hello"
    # Test with both strings empty
    assert concatenate_strings("", "") == ""


def test_list_index_error():
    # The function should routinely return the first element (1) of the list.
    result = list_index_error()
    assert result == 1
```