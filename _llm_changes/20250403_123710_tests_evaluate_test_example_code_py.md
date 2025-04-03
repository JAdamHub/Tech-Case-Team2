---
layout: llm_change
title: "Generated Tests for example_code.py"
date: 2025-04-03T12:37:10.931118
file: "tests/evaluate/test_example_code.py"
change_type: "Test Generation"
source_file: "evaluate/example_code.py"
consolidated: true
---
```python
import pytest
from evaluate.example_code import add, subtract, multiply, divide, buggy_function, another_function, faulty_logic

# Tests for add(a, b)
def test_add():
    # Typical cases
    assert add(1, 2) == 3
    assert add(10, 15) == 25
    # Using zero
    assert add(0, 0) == 0
    # Negative numbers
    assert add(-1, -2) == -3
    # Mixed sign
    assert add(-5, 10) == 5

# Tests for subtract(a, b)
def test_subtract():
    # Typical cases
    assert subtract(5, 2) == 3
    # Negative result
    assert subtract(2, 5) == -3
    # Zero values
    assert subtract(0, 0) == 0
    # Negative numbers
    assert subtract(-3, -1) == -2
    # Mixed sign
    assert subtract(5, -3) == 8

# Tests for multiply(a, b)
def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    # Multiplication with zero
    assert multiply(0, 100) == 0
    # Negative numbers
    assert multiply(-2, 3) == -6
    # Two negatives
    assert multiply(-4, -5) == 20
    # Multiplying with one
    assert multiply(1, 7) == 7

# Tests for divide(a, b)
def test_divide():
    # Typical division
    assert divide(10, 2) == 5
    # Division resulting in a float
    assert divide(7, 2) == 3.5
    # Division with negative numbers
    assert divide(-6, 2) == -3
    # Division with both negative numbers
    assert divide(-6, -2) == 3
    # Boundary case: division by zero raises ValueError
    with pytest.raises(ValueError):
        divide(10, 0)

# Tests for buggy_function(x)
def test_buggy_function():
    # Expect a ZeroDivisionError regardless of the input
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)
    with pytest.raises(ZeroDivisionError):
        buggy_function(-5)

# Tests for another_function(a, b)
def test_another_function():
    # Typical cases (similar to add)
    assert another_function(2, 3) == 5
    assert another_function(20, -5) == 15
    # Check identity with add for zero values
    assert another_function(0, 0) == 0
    # More cases
    assert another_function(-10, -15) == -25

# Tests for faulty_logic(a, b)
def test_faulty_logic():
    # Case when a > b: function returns (b - a)
    result = faulty_logic(5, 3)
    assert result == (3 - 5)  # Expected: -2

    # Case when a < b: function returns (a - b)
    result = faulty_logic(3, 5)
    assert result == (3 - 5)  # Expected: -2

    # Case when a == b: returns zero (a - b)
    result = faulty_logic(4, 4)
    assert result == 0

    # Additional edge case
    result = faulty_logic(-2, -5)
    # Since -2 > -5 is True, it returns (-5 - (-2)) = -3
    assert result == -3
```