# example.py
import meTal

def decorator1(func):
    def wrapper(*args, **kwargs):
        print("Decorator 1")
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    def wrapper(*args, **kwargs):
        print("Decorator 2")
        return func(*args, **kwargs)
    return wrapper

# Use a module with decorator1 meTal applied
with meTal(decorator1):
    import simple
    simple.hello('Guido')

# Use a module with decorator2 meTal applied
with meTal(decorator2):
    import simple
    simple.hello('Guido')

# Use a module with decorator1 and decorator2 meTal applied
with meTal(decorator1), meTal(decorator2):
    import simple
    simple.hello('Guido')
