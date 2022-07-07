"""
Iterator has a next() method which is called everytime a value is to be fetched. Once all values are fetched if still
the next() method is called then we will get a StopIteration Exception.

Iterator can be created by using an iter() function.
"""
a = [1, 2]
#
# a = iter(a)
#
# print(next(a))
# print(next(a))
# print(next(a))



"""
How the for loop works:
we pass on an iterable and python creates an iterator by passing it over the iter() func. 
Then it calls the next() func to get the next element everytime.
Terminates the loop once the stopIteration exception is raised and stops the iteration.
"""
for i in a:
    print(i)


