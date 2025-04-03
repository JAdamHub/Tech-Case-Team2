import pytest
from evaluate."buggy copy" import add_numbers, subtract_numbers, multiply_numbers, divide_numbers, concatenate_strings, list_index_error

def test_add_numbers():
    # Typical integer addition.
    assert add_numbers(2, 3) == 5
    # Addition with negative numbers.
    assert add_numbers(-4, 2) == -2
    # Addition with floats.
    assert add_numbers(2.5, 3.5) == 6.0
    # Addition with zero.
    assert add_numbers(0, 5) == 5

def test_subtract_numbers():
    # Typical subtraction.
    assert subtract_numbers(10, 5) == 5
    # Subtraction resulting in negative.
    assert subtract_numbers(5, 10) == -5
    # Subtraction with zero.
    assert subtract_numbers(0, 3) == -3
    # Subtraction with floats.
    assert subtract_numbers(5.5, 2.5) == 3.0

def test_multiply_numbers():
    # Typical multiplication.
    assert multiply_numbers(3, 4) == 12
    # Multiplication with zero.
    assert multiply_numbers(0, 100) == 0
    # Multiplication with negative numbers.
    assert multiply_numbers(-3, 5) == -15
    # Multiplication with floats.
    assert multiply_numbers(2.5, 4) == 10.0

def test_divide_numbers():
    # Typical division.
    assert divide_numbers(10, 2) == 5
    # Division with floats.
    assert divide_numbers(7.5, 2.5) == 3.0
    # Edge: division of a negative number.
    assert divide_numbers(-12, 3) == -4
    # Test division by zero raises ZeroDivisionError.
    with pytest.raises(ZeroDivisionError):
        divide_numbers(10, 0)

def test_concatenate_strings():
    # Typical string concatenation.
    assert concatenate_strings("Hello", "World") == "HelloWorld"
    # Concatenation with empty strings.
    assert concatenate_strings("", "Test") == "Test"
    assert concatenate_strings("Test", "") == "Test"
    # Concatenation of two empty strings results in empty string.
    assert concatenate_strings("", "") == ""
    # Concatenation with spaces.
    assert concatenate_strings("Hello ", "World") == "Hello World"

def test_list_index_error():
    # The function should return the first element of the list [1, 2, 3], which is 1.
    assert list_index_error() == 1