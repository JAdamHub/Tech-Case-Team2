---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for buggy.py"
date: 2025-04-03T10:59:43.371703
file: "tests/evaluate/test_buggy.py" # Report is about the test file
change_type: "Test Generation"
source_file: "evaluate/buggy.py"
---
```python
import builtins
# Override input so that when evaluate.buggy is imported, it does not wait for user input.
builtins.input = lambda prompt: "0"

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
    # Typical integer addition
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    # Float addition
    assert add_numbers(2.5, 3.5) == 6.0
    # Edge case: adding zeros
    assert add_numbers(0, 0) == 0

def test_subtract_numbers():
    # subtract_numbers is buggy because it refers to an undefined variable 'c'
    with pytest.raises(NameError):
        subtract_numbers(5, 3)

def test_multiply_numbers():
    # Typical multiplication
    assert multiply_numbers(2, 3) == 6
    # Multiplying by zero
    assert multiply_numbers(0, 10) == 0
    # Negative numbers multiplication
    assert multiply_numbers(-2, 3) == -6

def test_divide_numbers():
    # divide_numbers always divides by zero, so it should trigger a ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 2)

def test_concatenate_strings():
    # concatenate_strings is buggy because it refers to an undefined variable 's3'
    with pytest.raises(NameError):
        concatenate_strings("hello", "world")

def test_list_index_error():
    # list_index_error attempts to access an out-of-range index, which should raise an IndexError.
    with pytest.raises(IndexError):
        list_index_error()
```