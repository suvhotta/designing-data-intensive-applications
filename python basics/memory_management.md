- In Python each object can have lots of names.
- A name is a label for an object.

###Types of objects:
- Simple objets: Numbers and strings
- Containers: dict, list, user defined classes 
- Simple objects are stored in memory only once.
    Example: `x = 300, y = 300` There would be only a single object with value 300 and two references would be created 
    for that object named as x, y. This can be checked by using the `id` function. However, if it is run in the REPL 
    then the results might be a bit different because REPL does a bit of pre-mature optimization and stroes
- If we create a container as `z = [300, 300]` Then the reference count to the object with value 300 would be 4 now.
  (2 created in above for x, y and 2 now for those present in the container)
    In this way the number of references to the object with val 300 increases.
- Again if we change the values of x and y to string values: `x='a', y='b'` then the total references of the object with 
    value 300 decreases by 2.


### What is reference?
- A name/container object that points to another object.

### What does the del statement do?
- It doesn't live up to its name i.e. it doesn't delete objects, rather it removes the name as a reference to that
    object. It reduces the ref count by 1.


### When is object removed from memory?
- When there are no more references to the object, it can be safely removed from the memory.
- It is an issue with global namespaces that those object's ref count may never be 0, thus the objects can never be freed.


## Internal Representation
- All objects in python inherit the PyObject struct. Which has fields for type and refcount.
- Python objects are stored in a private heap. The management of this heap is done by python memory manager. Internally,
    there are object specific allocators to deal with objects of the same type.
- Python variable names are stored in a stack. These are contiguous memory locations and the allocation happens in the\
    function call stack. Whenever a function is called, it is added onto the program's call stack.


## Garbage Collection in Python:
1. Reference collection: Add/remove references varies the ref count. When the refcount reaches 0, remove that object.
    It is not generally thread-safe. To make it thread-safe the concept of GIL was introduced in cPython.
    However, reference counting by default doesn't detect cyclical references.
2. Generational garbage collection: Python assigns generations to objects based on certain criteria. Whenever number of 
    objects in certain generation reaches a threshold, python runs a garbage collection algorithm on that generation and
    all subsequent younger ones. During this process any cyclical references are checked.

- When the ref count reaches 0, the objects are cleaned up immediately. If however, they've cycles then we will have to
   wait till generational garbage collection happens.

## Why memory doesn't get freed after garbage collection in python?
- When memory is freed, it is in a fragmented form and not in contiguous memory locations since heap is fragmented.
- The freed memory is released back to python interpreter and not necessarily to the OS back.