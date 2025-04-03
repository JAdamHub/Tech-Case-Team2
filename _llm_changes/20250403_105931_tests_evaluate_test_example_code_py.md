---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T10:59:31.759879
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
    assert add(10, 15) == 25
    # Edge cases with negatives and zero
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    # Float inputs
    assert add(1.5, 2.5) == 4.0

def test_subtract():
    # Typical cases
    assert subtract(10, 5) == 5
    assert subtract(100, 50) == 50
    # Edge cases with negatives and zero
    assert subtract(-1, -1) == 0
    assert subtract(0, 5) == -5
    # Mixed sign
    assert subtract(-5, 5) == -10

def test_multiply():
    # Typical cases
    assert multiply(2, 3) == 6
    assert multiply(4, 5) == 20
    # Cases with zero and negatives
    assert multiply(0, 5) == 0
    assert multiply(-1, 10) == -10
    # Float multiplication
    assert multiply(1.5, 2) == 3.0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    # Cases with negatives and floats
    assert divide(-10, 2) == -5
    assert divide(5, -2) == -2.5
    # Error case: division by zero
    with pytest.raises(ValueError):
        divide(5, 0)

def test_buggy_function():
    # This function is designed to always raise ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    # Test with zero input.
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # Typical addition
    assert another_function(3, 4) == 7
    assert another_function(10, 15) == 25
    # Edge cases with negatives and zero
    assert another_function(-1, -1) == -2
    assert another_function(0, 0) == 0
    # Float addition
    assert another_function(1.1, 2.2) == 3.3

def test_faulty_logic():
    # Testing when a > b: according to the faulty logic, returns b - a.
    result = faulty_logic(10, 5)
    assert result == (5 - 10)  # Expected -5

    # Testing when a < b: returns a - b.
    result = faulty_logic(5, 10)
    assert result == (5 - 10)  # Expected -5

    # Testing when a == b: returns a - b which should be 0.
    result = faulty_logic(5, 5)
    assert result == 0

    # Additional test: when negatives are involved.
    result = faulty_logic(-3, 2)
    # Here, -3 < 2, so expected result is -3 - 2 = -5.
    assert result == -5

    result = faulty_logic(2, -3)
    # Here, 2 > -3, so expected result is -3 - 2 = -5.
    assert result == -5
```