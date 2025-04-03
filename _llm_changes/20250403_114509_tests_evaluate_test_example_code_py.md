---
layout: llm_change
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:45:09.954784
file: "tests/evaluate/test_example_code.py"
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
    assert add(1, 2) == 3
    assert add(-1, 5) == 4
    assert add(0, 0) == 0
    # Floating point numbers
    assert add(1.5, 2.5) == 4.0

def test_subtract():
    # Typical cases
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0
    # Floating point numbers
    assert subtract(2.5, 1.5) == 1.0

def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-3, 4) == -12
    # Edge case: multiplying by zero
    assert multiply(0, 10) == 0
    # Floating point numbers
    assert multiply(2.5, 4) == 10.0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(-9, 3) == -3
    # Floating point numbers
    assert divide(7.5, 2.5) == 3.0
    # Error condition: division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(5, 0)

def test_buggy_function():
    # This function is intentionally buggy and should raise a ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        buggy_function(100)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # Similar to add, these tests ensure typical behavior
    assert another_function(1, 2) == 3
    assert another_function(-5, 3) == -2
    assert another_function(0, 0) == 0

def test_faulty_logic():
    # Test when a > b: faulty_logic returns b - a (which may be considered incorrect)
    # For example, for a=10 and b=3, the function returns 3 - 10 = -7.
    assert faulty_logic(10, 3) == -7

    # Test when a <= b: faulty_logic returns a - b normally.
    assert faulty_logic(3, 10) == (3 - 10)
    
    # Test when a equals b: should return 0.
    assert faulty_logic(5, 5) == (5 - 5)
```