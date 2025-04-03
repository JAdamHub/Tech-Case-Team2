---
layout: llm_change
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:51:28.105622
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

# Tests for add(a, b)
def test_add():
    # Typical cases
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    # Float values
    assert add(2.5, 3.5) == 6.0
    # Edge: adding zero
    assert add(0, 0) == 0


# Tests for subtract(a, b)
def test_subtract():
    # Typical cases
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    # Zero subtraction
    assert subtract(0, 0) == 0
    # Negative numbers
    assert subtract(-3, -2) == -1


# Tests for multiply(a, b)
def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-3, 4) == -12
    # Multiply by zero
    assert multiply(0, 100) == 0
    # Float multiplication
    assert multiply(2.5, 4) == 10.0


# Tests for divide(a, b)
def test_divide():
    # Typical cases
    assert divide(10, 2) == 5
    # Float division
    assert divide(7, 2) == 3.5
    # Division with negative numbers
    assert divide(-10, 2) == -5
    # Edge case: division by a fraction
    assert divide(5, 0.5) == 10

    # Error condition: division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(10, 0)


# Tests for buggy_function(x)
def test_buggy_function():
    # Since buggy_function always causes a ZeroDivisionError regardless of the input,
    # testing with any input should raise the exception.
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)


# Tests for another_function(a, b)
def test_another_function():
    # Typical cases (similar to add)
    assert another_function(1, 2) == 3
    assert another_function(-1, 1) == 0
    # Edge: adding zeros
    assert another_function(0, 0) == 0


# Tests for faulty_logic(a, b)
def test_faulty_logic():
    # When a > b, according to the faulty logic: returns b - a
    assert faulty_logic(10, 5) == 5 - 10  # Expected: -5

    # When a < b, the function returns a - b
    assert faulty_logic(5, 10) == 5 - 10  # Expected: -5

    # When a == b, falls to else clause: a - b which is zero
    assert faulty_logic(7, 7) == 0

    # Additional test: check consistency with both branches
    # Test that the result is not the positive difference
    result1 = faulty_logic(15, 10)  # Expected: 10 - 15 = -5, not 5
    result2 = faulty_logic(10, 15)  # Expected: 10 - 15 = -5
    assert result1 == result2 == -5
```