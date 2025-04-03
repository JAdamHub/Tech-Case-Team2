---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:12:45.433801
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
    # Edge cases
    assert add(0, 0) == 0
    assert add(100, 200) == 300

def test_subtract():
    # Typical cases
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    # Edge cases
    assert subtract(0, 0) == 0
    assert subtract(-2, -3) == 1

def test_multiply():
    # Typical cases
    assert multiply(4, 3) == 12
    assert multiply(-2, 3) == -6
    # Edge cases
    assert multiply(0, 10) == 0
    assert multiply(0, 0) == 0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(-9, 3) == -3
    # Edge cases: division resulting in float
    assert divide(7, 2) == 3.5
    # Error conditions: division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(10, 0)

def test_buggy_function():
    # This function intentionally causes a ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        buggy_function(5)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # Typical cases (similar to add)
    assert another_function(2, 3) == 5
    assert another_function(-1, 1) == 0
    # Edge cases
    assert another_function(0, 0) == 0
    assert another_function(100, 200) == 300

def test_faulty_logic():
    # Check behavior for a > b, expecting b - a based on the implementation
    result = faulty_logic(5, 3)
    # According to the faulty logic, if a > b then it returns b - a,
    # so for (5, 3) we expect 3 - 5 = -2
    assert result == -2

    # Check behavior for a <= b, it returns a - b 
    result = faulty_logic(3, 5)
    # For (3, 5) we expect 3 - 5 = -2 as per the implementation
    assert result == -2

    # Check when a equals b, should return a - b = 0
    result = faulty_logic(4, 4)
    assert result == 0
```