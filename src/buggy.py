# This script contains multiple functions with intentional errors

def add_numbers(a, b):
    return a + b  # Works correctly

def subtract_numbers(a, b):
    return a - c  # 'c' is undefined

def multiply_numbers(a, b):
    return a * b  # Works correctly

def divide_numbers(a, b):
    return a / 0  # Division by zero error

def concatenate_strings(s1, s2):
    return s1 + s3  # 's3' is undefined

def list_index_error():
    my_list = [1, 2, 3]
    return my_list[5]  # Index out of range

# User input
a = input("Enter a number: ")
b = input("Enter another number: ")
print("Addition:", add_numbers(a, b))
print("Subtraction:", subtract_numbers(a, b))
print("Multiplication:", multiply_numbers(a, b))
print("Division:", divide_numbers(a, b))