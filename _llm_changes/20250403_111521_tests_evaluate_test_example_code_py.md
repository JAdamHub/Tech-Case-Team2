---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T11:15:21.733547
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

# Test for add(a, b)
def test_add():
    # Typical cases
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    # Edge case
    assert add(0, 0) == 0
    # Large numbers
    assert add(100000, 200000) == 300000

# Test for subtract(a, b)
def test_subtract():
    # Typical cases
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    # Edge case: subtracting zero
    assert subtract(0, 10) == -10
    assert subtract(10, 0) == 10

# Test for multiply(a, b)
def test_multiply():
    # Typical cases
    assert multiply(4, 5) == 20
    assert multiply(-4, 5) == -20
    # Edge case: one of the factors is zero
    assert multiply(0, 10) == 0
    assert multiply(10, 0) == 0
    # Multiplying negatives
    assert multiply(-3, -3) == 9

# Test for divide(a, b)
def test_divide():
    # Typical case
    assert divide(10, 2) == 5
    # Division resulting in float
    assert divide(7, 2) == 3.5
    # Edge case: dividing by negative number
    assert divide(10, -2) == -5
    # Error condition: division by zero should raise ValueError
    with pytest.raises(ValueError):
        divide(10, 0)

# Test for buggy_function(x)
def test_buggy_function():
    # Calling buggy_function should always raise ZeroDivisionError because of division by zero.
    with pytest.raises(ZeroDivisionError):
        buggy_function(5)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

# Test for another_function(a, b)
def test_another_function():
    # Since another_function simply returns a + b, tests similar to add.
    assert another_function(1, 2) == 3
    assert another_function(-1, -2) == -3
    assert another_function(0, 0) == 0

# Test for faulty_logic(a, b)
def test_faulty_logic():
    # This function implements logic that may be incorrect.
    # When a > b, it returns b - a (which is negative).
    # When a <= b, it returns a - b.
    # Testing both scenarios:
    
    # Case where a > b
    result = faulty_logic(5, 3)
    # Expected based on the provided implementation: 3 - 5 = -2
    assert result == -2, f"Expected -2 when a > b, got {result}"
    
    # Case where a == b: both paths yield the same result.
    result = faulty_logic(4, 4)
    # expected: 4 - 4 = 0
    assert result == 0, f"Expected 0 when a == b, got {result}"
    
    # Case where a < b
    result = faulty_logic(2, 5)
    # Expected based on implementation: 2 - 5 = -3
    assert result == -3, f"Expected -3 when a < b, got {result}"
    
    # Additional boundary check
    result = faulty_logic(-1, -5)
    # Here, a > b because -1 > -5, so it returns -5 - (-1) = -4.
    assert result == -4, f"Expected -4 for faulty_logic(-1,-5), got {result}"
```