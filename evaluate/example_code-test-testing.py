def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Introduce a bug
def buggy_function(x):
    return x / 0  # This will raise a ZeroDivisionError

# Introduce linter errors
def another_function( a ,b ):
    return a+b

# Introduce another bug
def faulty_logic(a, b):
    if a > b:
        return b - a  # This logic might be incorrect based on the intended functionality
    return a - b