"""
Generator is a special kind of function which gives a lazy iterator and uses yield keyword.
"""

# def indefinite_sequence():
#     num = 0
#     while True:
#         yield num
#         num += 1
#
# for i in indefinite_sequence():
#     print(i)
#     if i > 50:
#         break


"""
Yield doesn't exit the function like return does. Yield just suspends the function execution and returns the yielded
value to the caller. When a func execution is suspended its state and all is saved for further usage.
"""

def multi_yield():
    yield_str = "1st yield"
    yield yield_str
    yield_str = "2nd yield"
    yield yield_str


new_yield = multi_yield()
print(next(new_yield))
print(next(new_yield))
