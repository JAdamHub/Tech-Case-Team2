---
layout: llm_change
title: "Generated Tests for buggy.py"
date: 2025-04-03T11:51:39.731229
file: "tests/evaluate/test_buggy.py"
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
    # Typical cases
    assert add_numbers(1, 2) == 3
    assert add_numbers(-5, 5) == 0
    # Edge cases: adding zeros
    assert add_numbers(0, 0) == 0
    # Floating point numbers
    assert add_numbers(2.5, 3.5) == 6.0


def test_subtract_numbers():
    # Typical subtraction
    assert subtract_numbers(10, 5) == 5
    assert subtract_numbers(-3, -3) == 0
    # Edge case: subtracting zero
    assert subtract_numbers(0, 5) == -5
    # Floating point result
    assert subtract_numbers(5.5, 2.0) == 3.5


def test_multiply_numbers():
    # Typical multiplication
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-2, 3) == -6
    # Edge case: multiplying by zero
    assert multiply_numbers(0, 100) == 0
    # Multiplying floats
    assert multiply_numbers(2.5, 4) == 10.0


def test_divide_numbers():
    # Typical division
    assert divide_numbers(10, 2) == 5
    # Division resulting in floats
    assert divide_numbers(7, 2) == 3.5

    # Edge case: dividing by a fraction
    assert divide_numbers(5, 0.5) == 10

    # Error condition: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(5, 0)


def test_concatenate_strings():
    # Typical string concatenation
    assert concatenate_strings("hello", "world") == "helloworld"
    # Edge cases: one or both strings empty
    assert concatenate_strings("", "world") == "world"
    assert concatenate_strings("test", "") == "test"
    assert concatenate_strings("", "") == ""


def test_list_index_error():
    # The function should safely return a valid element (first element) from the list
    result = list_index_error()
    # Given the implementation, the expected element is 1 (from [1, 2, 3])
    assert result == 1
```