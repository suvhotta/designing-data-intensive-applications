## How does the computer run any program?
- The processor runs some machine code instructions stored in the memory(RAM).
- These instructions are binary and written in a processor specific manner. Example: the list of instructions for an 
   intel processor are different from those for an ARM processor.


## Compiled and Interpreted Languages:
- Depending on how the source code is converted into binary code/machine code, languages are broadly classified into 2 
    types: compiled languages and interpreted languages.


### Compiled Language:
- There is a program called as compiler which converts the source code into binary and then the binary is an executable. 
   The source code isn't any longer required.
- Ready to run once compiled. 
- Not cross-platform. The machine level code will be different for different processors.
- Often faster
- Source code isn't required to be sent over and over again.
example: C, C++


### Interpreted Language:
- An interpreted langauge like javascript on the other hand translates the source code into machine code everytime on 
    the fly. That's why in the browser the source code of js is being sent and the interpreter present in the browser
    translates it to machine code.
- It is cross-platform as the source code is directly sent and there are separate interpreters on an env basis which
    convert it to the appropriate machine code.
- Easier to debug as always have access to source code.
- It is slower.
- The source code isn't private.
example: PHP, JavaScript

  
## How python runs the source code?
- The source code which we write are usually human-readable and not meant for processor to execute.
- We run a program by typing `python <filename.py>`. Here 'python' refers to the python interpreter which itself is a
    binary. The python interpreter will be the actual program that will be running and to that we pass on the 
    source code file location.
- The python interpreter packs 2 things: PVM and the compiler.
- The compiler converts the actual source code into an intermediary format known as byte code. This byte code is machine
    independent and is not something which the processor will directly consume.
- The byte code is intended for the PVM(python virtual machine). The PVM reads the instructions of the bytecode and
    executes on the hardware. So this interpreter is actually different for different processors and that differentiates
    how the PVM would execute the same piece of byte code.
- In this way its clear that python isn't just any interpreted language it is actually a mixed bag of both compiler and
    interpreter.
- 