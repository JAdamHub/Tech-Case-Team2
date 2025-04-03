---
layout: llm_change
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:35:45.389162
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
    faulty_logic
)

def test_add():
    # Typical cases
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    # Edge case: adding zeros
    assert add(0, 0) == 0

def test_subtract():
    # Typical cases
    assert subtract(10, 5) == 5
    assert subtract(-1, -1) == 0
    # Edge case: subtracting zero
    assert subtract(5, 0) == 5

def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    # Edge cases: multiplication by zero
    assert multiply(0, 100) == 0
    assert multiply(0, 0) == 0

def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    assert divide(-9, 3) == -3
    # Edge case: division resulting in float
    result = divide(7, 2)
    assert result == 3.5
    # Error condition: division by zero
    with pytest.raises(ValueError) as exc_info:
        divide(5, 0)
    assert "Cannot divide by zero" in str(exc_info.value)

def test_buggy_function():
    # The function is designed to cause ZeroDivisionError
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

def test_another_function():
    # Typical cases similar to addition
    assert another_function(3, 7) == 10
    assert another_function(-3, -7) == -10
    # Edge case: mixing positive and negative values
    assert another_function(-5, 5) == 0

def test_faulty_logic():
    # When a is less than or equal to b, it should return a - b.
    assert faulty_logic(3, 5) == 3 - 5  # Expected: -2
    # When a is greater than b, according to the faulty logic, it returns b - a.
    assert faulty_logic(10, 4) == 4 - 10  # Expected: -6
    # Testing equality case: since a is not greater than b, should follow a - b.
    assert faulty_logic(5, 5) == 0
```