---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for buggy.py"
date: 2025-04-03T11:05:17.380532
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
    # Test with integers
    result = add_numbers(2, 3)
    assert result == 5, "Adding 2 and 3 should be 5"

    # Test with floats
    result = add_numbers(2.5, 3.5)
    assert result == 6.0, "Adding 2.5 and 3.5 should be 6.0"

    # Test with negative numbers
    result = add_numbers(-1, -9)
    assert result == -10, "Adding -1 and -9 should be -10"

    # Test with strings (concatenation)
    result = add_numbers("Hello, ", "world!")
    assert result == "Hello, world!", "Concatenating strings should work as expected"

def test_subtract_numbers():
    # Since subtract_numbers is buggy (it references an undefined variable 'c'),
    # we expect NameError to be raised.
    with pytest.raises(NameError):
        subtract_numbers(5, 3)

def test_multiply_numbers():
    # Test with integers
    result = multiply_numbers(3, 4)
    assert result == 12, "Multiplying 3 and 4 should be 12"

    # Test with zero
    result = multiply_numbers(0, 10)
    assert result == 0, "Multiplying any number with 0 should be 0"

    # Test with floats
    result = multiply_numbers(2.5, 4)
    assert result == 10.0, "Multiplying 2.5 and 4 should be 10.0"

def test_divide_numbers():
    # The divide_numbers function divides by 0 regardless of b.
    # Use pytest.raises for ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 2)

def test_concatenate_strings():
    # Since concatenate_strings is buggy (it references an undefined variable 's3'),
    # we expect a NameError to be raised.
    with pytest.raises(NameError):
        concatenate_strings("Hello, ", "world!")

def test_list_index_error():
    # list_index_error should raise an IndexError because it accesses an out-of-bound index.
    with pytest.raises(IndexError):
        list_index_error()
```