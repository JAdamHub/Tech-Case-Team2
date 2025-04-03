import pytest
from evaluate.buggy import (
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
    concatenate_strings,
    list_index_error,
)

def test_add_numbers():
    # Typical inputs: adding integers
    assert add_numbers(2, 3) == 5
    # Edge case: negative numbers
    assert add_numbers(-1, -1) == -2
    # Floating point numbers
    assert add_numbers(2.5, 3.5) == 6.0
    # Adding strings (should work for concatenation since '+' is valid for strings)
    assert add_numbers("Hello ", "World") == "Hello World"

def test_subtract_numbers():
    # This function has a bug: it uses an undefined variable 'c'
    with pytest.raises(NameError):
        subtract_numbers(5, 3)

def test_multiply_numbers():
    # Typical multiplication
    assert multiply_numbers(4, 5) == 20
    # Multiplication with zero
    assert multiply_numbers(0, 10) == 0
    # Multiplication with negative numbers
    assert multiply_numbers(-2, 3) == -6

def test_divide_numbers():
    # This function has a bug: it always divides by zero.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 2)
    with pytest.raises(ZeroDivisionError):
        divide_numbers(0, 3)

def test_concatenate_strings():
    # This function has a bug: it attempts to use an undefined variable 's3'
    with pytest.raises(NameError):
        concatenate_strings("foo", "bar")

def test_list_index_error():
    # This function has a bug: it accesses an out-of-range index in a list.
    with pytest.raises(IndexError):
        list_index_error()