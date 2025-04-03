---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T10:57:33.613311
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
    # Edge cases: zeros
    assert add(0, 0) == 0
    # Float addition
    assert add(2.5, 3.5) == 6.0

def test_subtract():
    # Typical cases
    assert subtract(10, 4) == 6
    assert subtract(4, 10) == -6
    # Edge cases: zeros
    assert subtract(0, 0) == 0
    # Float subtraction
    assert subtract(5.5, 2.5) == 3.0

def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    # Edge cases: multiplication with zero
    assert multiply(0, 100) == 0
    # Multiplication with floats
    assert multiply(2.0, 3.5) == 7.0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(-9, 3) == -3
    # Edge case: non-integer division
    assert divide(7, 2) == 3.5
    # Error condition: division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(5, 0)

def test_buggy_function():
    # buggy_function always raises ZeroDivisionError regardless of input.
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # another_function should behave like add
    assert another_function(1, 2) == 3
    assert another_function(-5, -5) == -10
    # Edge case
    assert another_function(0, 0) == 0
    # Float addition
    assert another_function(1.2, 3.4) == 4.6

def test_faulty_logic():
    # For a > b: faulty_logic returns b - a (which is likely not the intended behavior)
    result = faulty_logic(5, 3)
    assert result == -2, "For inputs (5, 3), expected faulty_logic to return 3 - 5 = -2"
    
    # For a <= b: faulty_logic returns a - b normally.
    result = faulty_logic(2, 5)
    assert result == -3, "For inputs (2, 5), expected faulty_logic to return 2 - 5 = -3"
    
    # Edge case: equality should follow the else branch
    result = faulty_logic(4, 4)
    assert result == 0, "For inputs (4, 4), expected faulty_logic to return 4 - 4 = 0"
```