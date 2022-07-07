"""
Functions are first class objects in python i.e. they can be passed as arguments to other functions.
"""
#
# def say_hello(name):
#     return f"Hello {name}"
#
# def greet_bob(greeter_func):
#     return greeter_func("Bob")
#
#
# print(greet_bob(say_hello))


"""
Inner function:
Those functions which are present inside other functions.

The inner functions aren't defined until the parent function is called.
The
"""

# def parent():
#     print("This is inside parent function")
#
#     def first_child():
#         print("This is first child function")
#
#     def second_child():
#         print("This is second child function")
#
#     first_child()
#     second_child()


# parent()


# def my_decorator(func):
#     def wrapper_func():
#         print("Do something before func execution")
#         func()
#         print("Do something after func execution")
#     return wrapper_func
#
#
# def hello():
#     print("Hello")
#
#
# hello = my_decorator(hello)



"""
Decorator wraps a function and modifies the behavior of the original function.

Instead of regular function passed to another function, python allows some syntactic sugar by using @ symbol.

hello = my_decorator(hello)
is same as 
@my_decorator
def hello()
"""
# import functools
#
# def do_twice(func):
#     @functools.wraps(func)
#     def wrapper_do_twice(*args, **kwargs):
#         func(*args, **kwargs)
#         return func(*args, **kwargs)
#     return wrapper_do_twice
#
#
# @do_twice
# def return_greeting(name):
#     print("Creating greeting")
#     return f"Hi {name}"
#
# print(return_greeting("jake"))
#
# print(return_greeting.__name__)




"""
Passing arguments to decorator.

For passing arguments to decorator, we need another wrapper layer on top of the existing 2 layers in the decorator.


It can be remembered like:
3 level of functions:
    1. Level 1 function for the args to the actual decorator.
    2. Level 2 function for passing the actual function as argument.
    3. Level 3 function for passing the actual function's arguments and kwargs.
"""



def my_decorator(*args, **kwargs):
    num_of_times = kwargs.get("num_times", 1)

    def wrapper(func):
        def _internal_func(*args, **kwargs):
            for _ in range(num_of_times):
                func(*args, **kwargs)
        return _internal_func
    return wrapper



@my_decorator(num_times=4)
def greet(name):
    print(f"Hello {name}")


greet("Suv")
