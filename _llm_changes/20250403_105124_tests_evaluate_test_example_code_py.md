---
layout: llm_change # Using the same layout, but could create a specific one
title: "Generated Tests for example_code.py"
date: 2025-04-03T10:51:24.584888
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

# Tests for add(a, b)
def test_add():
    # typical cases
    assert add(1, 2) == 3
    assert add(-1, -2) == -3
    # mixing positive and negative
    assert add(-1, 2) == 1
    # float values
    assert add(1.5, 2.5) == 4.0

# Tests for subtract(a, b)
def test_subtract():
    # typical cases
    assert subtract(10, 5) == 5
    assert subtract(5, 10) == -5
    # edge cases with zero
    assert subtract(0, 0) == 0
    # mixing negative values
    assert subtract(-5, -10) == 5

# Tests for multiply(a, b)
def test_multiply():
    # typical cases
    assert multiply(3, 4) == 12
    # multiplying by zero
    assert multiply(0, 100) == 0
    # negative numbers
    assert multiply(-3, 4) == -12
    # both negative
    assert multiply(-3, -4) == 12

# Tests for divide(a, b)
def test_divide():
    # typical division
    assert divide(10, 2) == 5
    # float division
    assert divide(7, 2) == 3.5
    # negative division
    assert divide(-9, 3) == -3
    # division with negative denominator
    assert divide(9, -3) == -3
    # edge case: division by a very small number (not zero)
    assert divide(5, 0.1) == 50
    # error condition: division by zero should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "Cannot divide by zero" in str(exc_info.value)

# Tests for buggy_function(x)
def test_buggy_function():
    # Since buggy_function always causes a ZeroDivisionError,
    # we expect that error regardless of the input.
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)
    with pytest.raises(ZeroDivisionError):
        buggy_function(-5)

# Tests for another_function(a, b)
def test_another_function():
    # similar to add, but provided as another function
    assert another_function(2, 3) == 5
    assert another_function(-2, -3) == -5
    assert another_function(2, -3) == -1
    # test with zero
    assert another_function(0, 5) == 5
    assert another_function(0, 0) == 0

# Tests for faulty_logic(a, b)
def test_faulty_logic():
    # When a > b, the function subtracts a from b (b - a)
    result = faulty_logic(10, 5)
    # Expected result with the faulty logic: 5 - 10 = -5
    assert result == -5, "For a > b, faulty_logic should return b - a."

    # When a <= b, the function returns a - b normally.
    result = faulty_logic(3, 7)
    assert result == (3 - 7), "For a <= b, faulty_logic should return a - b."
    
    # Equal values: should return zero (3 - 3)
    assert faulty_logic(3, 3) == 0

    # Additional edge case: negative numbers
    # if a > b even with negative numbers, e.g., (-2, -5) => -5 - (-2) = -3 
    result = faulty_logic(-2, -5)
    assert result == -3, "For a > b with negatives, faulty_logic should return b - a."
    
    # a == b for negatives
    assert faulty_logic(-4, -4) == 0
```