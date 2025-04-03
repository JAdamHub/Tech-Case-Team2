---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:05:08.904654
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
    assert add(1, 2) == 3
    assert add(-1, -2) == -3
    assert add(0, 0) == 0
    # Edge cases with floats
    assert add(1.5, 2.5) == 4.0

def test_subtract():
    # Typical cases
    assert subtract(5, 3) == 2
    assert subtract(-1, -2) == 1
    assert subtract(0, 5) == -5
    # Edge cases with floats
    assert subtract(5.5, 2.5) == 3.0

def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    # Multiplying by zero
    assert multiply(0, 10) == 0
    # Edge case with floats
    assert multiply(2.5, 4) == 10.0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(-9, 3) == -3
    # Division resulting in float
    assert divide(7, 2) == 3.5

    # Test division by zero raises ValueError
    with pytest.raises(ValueError):
        divide(10, 0)

def test_buggy_function():
    # Since buggy_function always divides by zero, it should raise ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        buggy_function(5)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # another_function should perform same as add
    assert another_function(2, 3) == 5
    assert another_function(-1, 1) == 0
    assert another_function(0, 0) == 0
    # With floats
    assert another_function(1.1, 2.2) == 3.3

def test_faulty_logic():
    # When a <= b, it behaves as subtract (a - b)
    assert faulty_logic(3, 5) == 3 - 5

    # When a > b, based on the function's logic it returns b - a
    # For example, for a=5 and b=3, the function returns 3 - 5 = -2 instead of 5 - 3
    assert faulty_logic(5, 3) == 3 - 5

    # Additional checks for boundary cases
    # When a == b, should fall into the else block (a - b)
    assert faulty_logic(4, 4) == 0
```