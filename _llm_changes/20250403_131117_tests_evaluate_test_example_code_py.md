---
layout: llm_change
title: "Generated Tests for example_code.py"
date: 2025-04-03T13:11:17.431582
file: "tests/evaluate/test_example_code.py"
change_type: "Test Generation"
source_file: "evaluate/example_code.py"
consolidated: true
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

# Tests for add(a, b)
def test_add():
    # Typical cases
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

    # Float inputs
    assert add(1.5, 2.5) == 4.0

    # Edge case: large numbers
    assert add(1_000_000, 2_000_000) == 3_000_000

# Tests for subtract(a, b)
def test_subtract():
    # Typical cases
    assert subtract(10, 5) == 5
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0

    # Negative result
    assert subtract(3, 5) == -2

    # Edge case: floats
    assert subtract(3.5, 1.2) == pytest.approx(2.3)

# Tests for multiply(a, b)
def test_multiply():
    # Typical cases
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6
    assert multiply(0, 100) == 0

    # Edge case: multiplication with floats
    assert multiply(2.5, 4) == 10.0

    # Large numbers
    assert multiply(1_000, 2_000) == 2_000_000

# Tests for divide(a, b)
def test_divide():
    # Typical division
    assert divide(10, 2) == 5
    assert divide(7, 2) == pytest.approx(3.5)
    assert divide(-10, 2) == -5

    # Division resulting in float
    assert divide(5, 2) == 2.5

    # Edge case: division with float numbers
    assert divide(5.0, 2.0) == 2.5

    # Error condition: division by zero
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "Cannot divide by zero" in str(exc_info.value)

# Tests for buggy_function(x)
def test_buggy_function():
    # This function is designed to always cause a ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

# Tests for another_function(a, b)
def test_another_function():
    # Typical cases (identical to add essentially)
    assert another_function(2, 3) == 5
    assert another_function(-1, 1) == 0
    assert another_function(0, 0) == 0

    # Float test
    assert another_function(1.5, 2.5) == 4.0

# Tests for faulty_logic(a, b)
def test_faulty_logic():
    # When a > b, the logic subtracts a from b.
    # For example: faulty_logic(5, 3) should return 3 - 5 = -2.
    assert faulty_logic(5, 3) == -2

    # When a <= b, it performs a - b normally.
    # For example: faulty_logic(3, 5) should return 3 - 5 = -2.
    assert faulty_logic(3, 5) == -2

    # Test equality condition: a == b should return 0
    assert faulty_logic(4, 4) == 0

    # Additional test to see potential unexpected behavior
    # a slightly greater than b
    assert faulty_logic(10, 9) == -1, "Expected faulty_logic to subtract larger number first when a > b"
```