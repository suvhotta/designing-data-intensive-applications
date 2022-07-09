"""
Variable scope:
LEGB
local: within function
enclosed: function within function
global: global variables
built-in: built-in variable/keywords

But the global variable can be changed by using global keyword.
There is a keyword nonlocal for enclosed variables.
"""

# var = 100
# def something():
#     global var
#     var += 1
#     print(var)
# something()
# print(var)


# def func():
#     var = 10
#     def nested():
#         nonlocal var
#         var += 1
#     nested()
#     print(var)
#
#
# func()

"""
Inheritance support in python:
It provides:
1. Single inheritance
2. Multiple inheritance
3. Multi level inheritance
"""

#
# class Child:
#
#     # Constructor
#     def __init__(self, name):
#         self.name = name
#
#     # To get name
#     def getName(self):
#         return self.name
#
#     # To check if this person is student
#     def isStudent(self):
#         return False
#
#
# # Derived class or Child class
# class Student(Child):
#
#     # True is returned
#     def isStudent(self):
#         return True
#
#     def getName(self):
#         return f"My name is: {self.name}"
#
#
#     # This is a pvt method
#     def __is_active(self):
#         return True
#
# s1 = Student("abc")
# print(s1.getName())

# Directly an instance of a class can't access a private method
# print(s1.__is_active())

# However, the same can be accessed through class name indirectly.
# print(s1._Student__is_active())
"""
Since python supports multiple inheritance, there is a concept of method resolution order(MRO).
MRO tells python how to search for inherited methods.
As per MRO, first it will search for a method in the actual class. Then in the first inherited class and its inherited
classes, then the second inherited class and its inherited classes and so on.
"""


"""
Lists:
- They are ordered.
- They can contain any arbitrary objects.
- List elements can be accessed by index.
- They can be nested to arbitrary depth.
- They are mutable.
- They are dynamic.
"""

# abc = [1, 2, 3]
# cd = [1, 2, 3]

# # Here == compares the values stored in both lists and hence they're equal
# print(abc == cd)
#
# # The memory address of the containers will be different because python creates separate containers every time.
# print(id(abc))
# print(id(cd))

# # The internals of the containers are still the same simple objects and hence they have the same memory location.
# print(id(abc[0]))
# print(id(cd[0]))

# cd = [1, 3, 2]

# As ordering matters in list, the objects are not equal.
# print(abc == cd)


# List can have arbitrary objects
# Lists can even contain complex objects, like functions, classes, and modules.
# a = [21.42, 'foobar', 3, 4, 'bark', False, 3.14159]

# Slicing
# If s is a string, s[:] returns a reference to the same object.
# If s is a list, s[:] returns a new list.
# a = [1, 2, 3, 4, 5, 6, 7, 8]
# print(a[3:0:-2])


# Lists support concatenation(+), replication(*) operators:
# abc = [1, 2, 3]
# print(abc+[4, 5])
# print(abc * 2)

# Lists support len, min, max
# len is O(1) operation
# max, min are O(n) operations.
# abc = ['foo', 'bar', 'baz', 'qux', 'quux', 'corge']
# print(max(abc))
# print(min(abc))
# Max, and min on a string list will give the lexical max and min of that list.


# abc = ['foo', 'bar', 'baz', 'qux', 'quux', 'corge', 'foo']
# abc.remove('foo')
# print(abc)
# abc.pop(1)
# remove method deletes based on the object passed.
# pop method deletes based on the index passed.
# pop returns the item that was removed.


"""
Tuple
- They are immutable.
- They're faster in interation than lists and also consume lesser memory.
- They're read only.
"""



"""
Set
- They are unordered.
- Elements are unique, duplicate elements aren't inserted.
- They can be modified, but the elements should be of immutable type. i.e. can't contain a list, dict
- Elements in a set can be of different type as long as they are immutable.

Time-complexities:
- Length, add, remove, in, not in, discard, pop --> all in O(1)
- Creation -> O(N), Depending on the size of the elements to be inserted.
"""

# s = 'abceef'
# # print(set(s))
# # Every time we create the set, the order of elements are different.
# s = set(s)
# abc = {'d', 'q', 'a', 'b'}
# # print(s | abc)
# # print(s.union(abc))
# # both of these give the union of the 2 sets.
#
#
# # print(s.intersection(abc))
# # gives the common of both sets
#
# abc.remove('d')
# print(abc)
#
# abc.discard('a')
# print(abc)

# Both remove and discard, removes element from the set but removes throws an exception if the element to be removed
# isn't present in the set.



"""
Dict
- The display order is in the same as they were defined.
- An object of any immutable type can be used as a dictionary key. Or rather something which can be hashable.
"""

d = {'a': 10, 'b': 20, 'c': 30}
# print(d.pop('b'))

# When we do a pop operation, the dict returns the value attached to that key.
# If the key is not present then it raises an exception, unless a default value is specified in the pop method.

print(d.popitem())
# Removes the last key-value pair added and returns it in form of tuple.
