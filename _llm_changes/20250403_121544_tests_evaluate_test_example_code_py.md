---
layout: llm_change
title: "Generated Tests for example_code.py"
date: 2025-04-03T12:15:44.141973
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
    faulty_logic
)

# Tests for add(a, b)
def test_add():
    # typical addition
    assert add(2, 3) == 5
    # addition with negative numbers
    assert add(-1, -1) == -2
    # addition with zero
    assert add(0, 5) == 5
    # addition with floats
    assert add(2.5, 3.5) == 6.0

# Tests for subtract(a, b)
def test_subtract():
    # typical subtraction
    assert subtract(10, 3) == 7
    # result might be negative
    assert subtract(3, 10) == -7
    # subtraction with zero
    assert subtract(5, 0) == 5
    # subtraction with floats
    assert subtract(5.5, 2.5) == 3.0

# Tests for multiply(a, b)
def test_multiply():
    # typical multiplication
    assert multiply(3, 4) == 12
    # multiplication with zero
    assert multiply(0, 100) == 0
    # multiplication with negative numbers
    assert multiply(-2, 3) == -6
    # multiplication with floats
    assert multiply(2.5, 4) == 10.0

# Tests for divide(a, b)
def test_divide():
    # typical division
    assert divide(10, 2) == 5
    # division resulting in float
    assert divide(5, 2) == 2.5
    # division with negative numbers
    assert divide(-9, 3) == -3
    # dividing by a number very close to zero (but not zero)
    assert divide(1, 0.1) == 10
    # division by zero should raise a ValueError
    with pytest.raises(ValueError):
        divide(5, 0)

# Tests for buggy_function(x)
def test_buggy_function():
    # calling buggy_function should raise a ZeroDivisionError regardless of input
    with pytest.raises(ZeroDivisionError):
        buggy_function(10)
    with pytest.raises(ZeroDivisionError):
        buggy_function(0)

# Tests for another_function(a, b)
def test_another_function():
    # similar behavior to add, typical case
    assert another_function(1, 2) == 3
    # with negatives
    assert another_function(-5, 5) == 0
    # with floats
    assert another_function(2.2, 3.3) == 5.5

# Tests for faulty_logic(a, b)
def test_faulty_logic():
    # When a is greater than b, logic returns b - a (which is negative)
    assert faulty_logic(10, 5) == (5 - 10)  # expected result: -5
    # When a is less than or equal to b, logic returns a - b
    assert faulty_logic(5, 10) == (5 - 10)  # expected result: -5
    # When a equals b, should follow the else branch
    assert faulty_logic(7, 7) == (7 - 7)    # expected result: 0
```