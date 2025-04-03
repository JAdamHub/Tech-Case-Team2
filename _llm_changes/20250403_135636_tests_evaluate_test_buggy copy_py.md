---
layout: llm_change
title: "Generated Tests for buggy copy.py"
date: 2025-04-03T13:56:36.625472
file: "tests/evaluate/test_buggy copy.py"
change_type: "Test Generation"
source_file: "evaluate/buggy copy.py"
consolidated: true
---
```python
import pytest

from evaluate.buggy_copy import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
    concatenate_strings,
    list_index_error,
)


def test_add_numbers():
    # Typical case: adding two positive integers
    assert add_numbers(2, 3) == 5

    # Case: adding negative numbers
    assert add_numbers(-1, -1) == -2

    # Edge case: adding zero
    assert add_numbers(0, 10) == 10


def test_subtract_numbers():
    # Typical case: subtracting two numbers
    assert subtract_numbers(10, 3) == 7

    # Case: subtracting a larger number from a smaller one (negative result)
    assert subtract_numbers(3, 10) == -7

    # Edge case: subtracting zero
    assert subtract_numbers(5, 0) == 5


def test_multiply_numbers():
    # Typical case: multiplication of two numbers
    assert multiply_numbers(4, 5) == 20

    # Edge case: multiplication by zero
    assert multiply_numbers(0, 10) == 0

    # Case: multiplication with a negative number
    assert multiply_numbers(-3, 6) == -18


def test_divide_numbers():
    # Typical case: division of two numbers
    assert divide_numbers(10, 2) == 5

    # Case: division that results in a float
    result = divide_numbers(7, 2)
    assert pytest.approx(result) == 3.5

    # Error condition: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(5, 0)


def test_concatenate_strings():
    # Typical case: concatenating two non-empty strings
    assert concatenate_strings("Hello, ", "world!") == "Hello, world!"

    # Edge case: concatenating with an empty string
    assert concatenate_strings("", "test") == "test"
    assert concatenate_strings("test", "") == "test"

    # Edge case: concatenating two empty strings
    assert concatenate_strings("", "") == ""


def test_list_index_error():
    # The function is expected to return the first element of the hard-coded list [1, 2, 3]
    assert list_index_error() == 1
```