---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:22:14.481960
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
    faulty_logic
)

def test_add():
    # Typical inputs
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    # Boundary and zero tests
    assert add(0, 0) == 0
    assert add(100, 200) == 300

def test_subtract():
    # Typical inputs
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    # Negative numbers
    assert subtract(-1, -1) == 0
    # Zero as an edge case
    assert subtract(0, 5) == -5

def test_multiply():
    # Typical inputs
    assert multiply(3, 4) == 12
    assert multiply(-1, 5) == -5
    # Multiplication with zero
    assert multiply(0, 100) == 0
    # Boundary test
    assert multiply(1, 0) == 0

def test_divide():
    # Typical input for division
    assert divide(10, 2) == 5
    assert divide(-9, 3) == -3
    # Floating point division check
    assert divide(5, 2) == pytest.approx(2.5)
    # Division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(10, 0)

def test_buggy_function():
    # buggy_function always divides by zero so it should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        buggy_function(5)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # Typical inputs; note this function behaves the same as add
    assert another_function(1, 2) == 3
    assert another_function(-1, -2) == -3
    # Sum with zero
    assert another_function(0, 5) == 5

def test_faulty_logic():
    # When a > b, the implemented logic returns b - a.
    # For example, with a=7 and b=3, we expect 3 - 7 = -4.
    assert faulty_logic(7, 3) == -4

    # When a <= b, it returns a - b. For example, with a=3 and b=7, we expect 3 - 7 = -4.
    assert faulty_logic(3, 7) == -4

    # When a equals b, it should return 0.
    assert faulty_logic(5, 5) == 0
```