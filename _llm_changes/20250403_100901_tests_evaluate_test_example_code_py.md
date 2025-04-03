---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T10:09:01.976984
file: "tests/evaluate/test_example_code.py" # Report is about the test file
change_type: "Test Generation"
source_file: "evaluate/example_code.py"
---
```python
import pytest
from evaluate.example_code import (
    add,
    subtract,
    multiply,
    divide,
    buggy_function,
    another_function,
    faulty_logic,
)

def test_add():
    # Typical cases
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(-5, -5) == -10
    # Edge case: adding zeros
    assert add(0, 0) == 0

def test_subtract():
    # Typical cases
    assert subtract(10, 5) == 5
    assert subtract(5, 10) == -5
    # Edge case: subtracting zero
    assert subtract(0, 0) == 0

def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-3, 4) == -12
    # Edge case: multiplication by zero
    assert multiply(0, 10) == 0
    assert multiply(0, 0) == 0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(5, 2) == 2.5
    # Edge case: division resulting in float
    assert divide(9, 3) == 3
    # Error condition: division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(5, 0)

def test_buggy_function():
    # This function is expected to raise ZeroDivisionError regardless of input
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    # Test with another value to ensure consistency
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # Typical cases similar to add, but ensure function works independently
    assert another_function(1, 2) == 3
    assert another_function(-2, 2) == 0
    # Edge case: both zeros
    assert another_function(0, 0) == 0

def test_faulty_logic():
    # Case where a > b: According to the faulty logic, it returns b - a.
    # For example, faulty_logic(5, 3) should return 3 - 5 = -2.
    assert faulty_logic(5, 3) == -2
    # Case where a <= b: It returns a - b.
    # For example, faulty_logic(3, 5) should return 3 - 5 = -2.
    assert faulty_logic(3, 5) == -2
    # Edge case: when a == b, both branches yield 0.
    assert faulty_logic(4, 4) == 0
```