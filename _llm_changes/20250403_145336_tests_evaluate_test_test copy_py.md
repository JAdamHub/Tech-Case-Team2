---
layout: llm_change
title: "Generated Tests for test copy.py"
date: 2025-04-03T14:53:36.311341
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
    list_index_error
)

def test_add_numbers():
    # Typical cases
    assert add_numbers(1, 2) == 3
    assert add_numbers(-1, 5) == 4
    # Edge cases: zeros and negatives
    assert add_numbers(0, 0) == 0
    assert add_numbers(-2, -3) == -5
    # Floating point numbers
    assert add_numbers(1.5, 2.5) == 4.0

def test_subtract_numbers():
    # Typical cases
    assert subtract_numbers(10, 5) == 5
    assert subtract_numbers(5, 10) == -5
    # Edge cases: zeros and negatives
    assert subtract_numbers(0, 0) == 0
    assert subtract_numbers(-5, -3) == -2
    # Floating point numbers
    assert subtract_numbers(2.5, 1.2) == pytest.approx(1.3)

def test_multiply_numbers():
    # Typical cases
    assert multiply_numbers(3, 4) == 12
    assert multiply_numbers(-2, 3) == -6
    # Edge cases: multiplication by zero
    assert multiply_numbers(0, 10) == 0
    # Multiplying negatives
    assert multiply_numbers(-3, -7) == 21
    # Floating point multiplication
    assert multiply_numbers(2.5, 4) == 10.0

def test_divide_numbers():
    # Typical cases
    assert divide_numbers(10, 2) == 5
    assert divide_numbers(-9, 3) == -3
    # Floating point division
    assert divide_numbers(7, 2) == pytest.approx(3.5)
    # Edge case: division resulting in a float
    assert divide_numbers(1, 3) == pytest.approx(0.3333333)
    
    # Error condition: division by zero should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_concatenate_strings():
    # Typical cases
    assert concatenate_strings("hello", "world") == "helloworld"
    # Edge cases: one or both strings empty
    assert concatenate_strings("", "world") == "world"
    assert concatenate_strings("hello", "") == "hello"
    assert concatenate_strings("", "") == ""
    # Concatenation of whitespace and characters
    assert concatenate_strings("foo", " bar") == "foo bar"

def test_list_index_error():
    # The function is expected to return the first element of the list [1, 2, 3]
    assert list_index_error() == 1
```