---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T12:15:57.115397
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
    # Typical cases
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 5) == 4

    # Edge cases with zero
    assert add_numbers(0, 0) == 0
    assert add_numbers(0, 5) == 5

    # Floating point addition
    assert add_numbers(0.1, 0.2) == pytest.approx(0.3)


def test_subtract_numbers():
    # Typical cases
    assert subtract_numbers(10, 5) == 5
    assert subtract_numbers(5, 10) == -5

    # Edge cases with zero
    assert subtract_numbers(0, 5) == -5
    assert subtract_numbers(5, 0) == 5

    # Subtraction with negative numbers
    assert subtract_numbers(-3, -2) == -1


def test_multiply_numbers():
    # Typical cases
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-2, 6) == -12

    # Multiplication with zero
    assert multiply_numbers(0, 10) == 0
    assert multiply_numbers(5, 0) == 0

    # Floating point multiplication
    assert multiply_numbers(2.5, 4) == 10.0


def test_divide_numbers():
    # Typical cases
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(7, 2) == 3.5

    # Division resulting in float when numbers are non-divisible
    result = divide_numbers(3, 2)
    assert isinstance(result, float)
    assert result == 1.5

    # Error condition: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(5, 0)


def test_concatenate_strings():
    # Typical concatenation
    assert concatenate_strings("Hello, ", "world!") == "Hello, world!"

    # Edge cases with empty strings
    assert concatenate_strings("", "Test") == "Test"
    assert concatenate_strings("Test", "") == "Test"
    assert concatenate_strings("", "") == ""

    # Concatenation of longer strings
    long_str1 = "Lorem ipsum "
    long_str2 = "dolor sit amet"
    assert concatenate_strings(long_str1, long_str2) == long_str1 + long_str2


def test_list_index_error():
    # This function should return the first element from the list [1, 2, 3]
    result = list_index_error()
    assert result == 1
```