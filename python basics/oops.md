## OOPS:
- Encapsulation: Restricting direct access to some attributes in a program.
    This can be achieved by writing getter and setters where rules can be defined
    for changing an attribute.(like a price of a product can never be a negative value is a valid check)
- Abstraction: Shows only the necessary attributes and hides the unnecessary information/details.
- Inheritance: If we have common scenarios they can be made reusable.
- Polymorphism: Single entity to be used in diff types in diff scenarios.

##Class:
- When searching for attributes, first it will check for instance attributes, 
  if not found then will go for class attributes.
- Once a class attribute is defined, every instance will get its own copy of 
    class attribute. So if some class attribute is changed for a particular instance,
    that won't change for any other instance.

## When to use class method and when static method?
- When a method has some relationship with the class, but not something that is unique 
    per instance.
- This should also do something that has a relationship with the class, but usually, those
    are used to manipulate different structures of data to instantiate objects.
- static methods don't pass the class argument as the first parameter to the method. While
    class methods do.
- static methods and class methods can be also called from an instance, but the requirements
    to do so is very rare.

## Property:
- Using a @property decorator we can create read only attributes.
- Using the property decorator we can do the getter, setter & deleter functionality.
