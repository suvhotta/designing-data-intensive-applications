## Constants:
- Integer ranges from -(2^31) to (2^31 - 1). It is also compiler and processor dependent.

## Main func:
- the return type of main func can be depending on the compiler.

## format specifier:
- while printing if  we are passing on variables to the std output then we need format specifiers. Those can be %f for real nums,
    %d for integers, %c for characters.

## Operators:
- Modulus operator(%) can't be used with float.
- Sign of modulus operator is always that of the numerator.(-5)%2 =-1 but 5%(-2) = 1.
- arithmetic operations also allowed on chars. However, that will be translated to be done on the ascii values instead of the actual chars.
- there is no exponent operator in c, it is instead done using the pow() func.

## Implicit type conversion:
- when a float val is stored in an int variable, the int variable doesn't have enough mem to do that. Hence it is truncated and type casted
    and only the integer part of it is stored. `int x = -3.5` result would be -3 and not -4.
- an op. between an int and int always will result in an int. 5/2 will give 2 and 2/9 will be 0.
- In an op. b/w real and int, int is first promoted to real and so it becomes a real and real op, and result is a real.
- `int k=2/9` and `int k=2.0/9` will both be 0 due to diff reasons. in first one, the val itself is 0 due to int/int. the second one, gives a
    float val but since stored in an int variable will give result as 0.
- If a char is directly compared with numbers, it's ascii value will be compared instead.

## Precedence of Operators:
- Pre increment/decrement operator: Right to left
- Post increment/decrement operator: Left to Right
- Assignment operator: Right to Left
- Arithmatic operator: Left to Right

## Pre-increment/Post-increment operator:
- in Pre-increment first val is increased by 1 and then assigned.
- in post-increment first assignment happens and then increment.

`int a=1, b; b = a++ + a++` this will give result as 3 the first a++ will still be 1 and the second one will be 2. 
`int a=1, b; b = ++a + ++a` this will be 6, as first there will be twice increment and then finally assigned 3 to each.

## Datatypes:
- there are 2 types of ints and chars, signed and unsigned. In signed, the sign is taken into account. The last digit(left-most)
    is reserved for the sign.(0 means positive, 1 means negative). 
- How is a negative num stored: -128: first the positive bit notation is done: (10000000) next its 1 compliment + 1 is done:
    which is 01111111 + 1 : 10000000.
- if we try to store -128 as an 8 bit num it can be done as shown above. However, if we attempt to store +128(10000000), due to
    the left most bit becoming a sign bit, this would be interpreted as -128. Hence the range is from -128 to +127 in case of signed
    char.

## Storage classes
- To completely define a variable we need both its datatype and its storage class.
- Storage class tells the following stuffs about a variable:
  - where it will be stored
  - default initial value of the variable
  - scope of the variable
  - life of the variable
- Automatic storage class:
  - stored in Memory(stack)
  - Default value: garbage value
  - Scope is local to where it is defined.
  - life is till it is in the scope where it is defined.
  - eg: `auto int i;`
- Register Storage Class:
  - stored in register
  - Default value: garbage value
  - Scope is local to where it is defined.
  - life is till it is in the scope where it is defined.
  - its access is faster than auto storage class. Hence whenever a variable is used at too many
    places, register is used.
  - But registers are limited in number and if they're all occupied then in that case, compiler
    will use auto and not throw any errors.
  - eg: `register int i;`
- Static Storage Class:
  - stored in mem(data segment)
  - default value: 0
  - Scope is local to where it is defined.
  - value of variable persists between func calls.
- Extern Storage Class:
  - stored in mem(data segment)
  - default val: 0
  - scope: global
  - life: as long as program execution doesn't end
  - if a variable is defined outside any func, by default its used as extern variable.
  - extern variables can be accessed by other files as well.

- the auto variables are defined in stack of mem, while static and extern are stored in data segment.


## C-preprocessor:
- It is a program that processes the c source code before it is being sent to the compiler.
- It pre-processes all the lines of code starting with '#'
- Its used for macro expansion, file inclusion etc.
  - Macro expansion
    - macro can be thought of as a template or a constant. It can also be like a small func. 
    - It is defined by #define <Macro_Name> val eg: `#define PI 3.142`
    - The macro name is always in uppercase.
    - A macro isn't a function hence return keyword can't be used.
    - A macro can replace a func. But the issue is that if we use a macro 100 times in the source code, it increases the
        size of the eventually compiled code. But a func takes more time and slows the program. This is avoided in macro as
        they've already been expanded. So there is a trade-off between memory space and time.
  - File Inclusion
    2 ways to include files:
    - \# include "filename"
      - This will look for files in the search path and also in the current working directory.
      - used for mostly user defined files.
    - \# include \<filename>
      - This will only look for files in the search path
      - Used for mostly library files/funcs.


## Functions:
- Before defining any function, first the prototype declaration is to be done. `void message();`
- Program execution always begins with `main()`. Main func can also be called from other funcs.
- Func can't be defined within another func.
- The default return type of any func is int. If we don't pass on any return type it will take int as the default one.
- The arguments sent from the calling funcs are called the actual arguments and those present in the called func are called formal arguments.
- `    int a = 1;
    printf("\n%d %d %d", a, ++a, a++);` the value of this code might be 1 2 2 or 3 3 1 depending on compiler. The order in which args are being passed 
    to a func varies from compiler to compiler and is not something specified by the programming language. If the same is passed from left to right, we
    get the first output and from right to left then we get the second output.

## Pointers
- `int i=3;` This declaration tells the compiler to reserve a space in mem to hold the integer value and associate the name i with this mem location.
    Store the value 3 at this location.
- & is the address of operator. * is called the value at address of pointer. so, *(&i) is same as writing i. *j is to be read as **Value at address stored at j**
- Whenever we are declaring any variable used to store an address, it is declared like `int *j; j=&i` this means that j stores the address of i and the 
    value stored at the address pointed by j is an integer value. During the declaration, the * tells that it stores an address.
- The pointer variables can be of different types depending on what kind of values they point to. But since all types of pointer variables store addresses,
    their size is always the same in the same compiler.
- If a pointer is incremented using a `++` operator then it will point to the next memory location of that type.
- Pointer can point to the mem location of array elements. `int *ptr; ptr=&arr[0]` this will point the pointer to the mem address of the first element of arr.
    The incr and decr of pointers through ptr++, ptr-- will in turn incr/decr mem locations of the arr.
- The following arithmatic operations can be performed on pointers:
  - Addition of a num to a pointer
  - Subtraction of a num from a pointer
  - Subtraction of a pointer from another
  - Comparison of 2 pointer variables.
- Usages of pointers:
  - To return multiple values from a func.
  - Whenever a large object exists, it is better to pass by reference to save memory.
  



## Arrays:
- Arrays can have only elements of the same datatype.
- In memory, the elements of array are placed adjacent to each other.
- While storing values, if we go outside the size of the array, it won't give any errors. But instead would keep those values
    at some other location. If something is already present there, it may get overwritten.
- ### Multi-dimensional arrays:
  - In multi dimensional arrays, in mem the elements are stored like a series of arrays. for eg: arr[3][2], first the 2 elements of first row are stored in mem,
    followed by the 2 elements of row 2, and then row 3.
  - Using pointers this can be generalized as arr[i][j]=*(*(arr+i)+j)
- ### Array of Pointers:
  - like array of ints, chars, etc. there can be also array of pointers.
  - it is defined as: `int *p[2]` this would be an array of integer pointers.
  - https://www.youtube.com/watch?v=ibj_AKOxpHo
  - 


## Dynamic Memory allocation
- malloc is a std lib func in c that is used to dynamically assign mem. It is a part of stdlib.h
- Malloc allocates requested size and returns a pointer. We need to capture this pointer. `int *arr = malloc(sizeof(int)*max)`
- Once the memory has been allocated, it needs to be freed before the program closes to avoid any memory leaks, using `free(arr)`function.