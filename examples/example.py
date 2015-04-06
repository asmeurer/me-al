# example.py

import meTal

def decorator(func):
    def wrapper(*args, **kwargs):
        print("Decorator")
        return func(*args, **kwargs)
    return wrapper

# Apply meTal to the module
with meTal(decorator):
    import simple

# Call the module with meTal applied
simple.hello('Guido')

# Import the module without meTal
import simple
simple.hello('Guido')
