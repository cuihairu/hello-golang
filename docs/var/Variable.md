A variable is the basic construct for storing and manipulating data. Its meaning has shifted several times across language paradigms; this page walks through it in four parts: role, evolution, type management, and paradigm.

### The basic role of variables

1. **Data storage**:
   - Variables hold the data a program needs while it runs. That data can be numbers, strings, booleans, objects, and so on.
   - Variables give that data a name, which makes it easier for the program to refer to and manipulate it.

2. **Data manipulation**:
   - Variables take part in various operations, such as arithmetic, logic, and string manipulation.
   - Through variables, a program can implement complex data-processing logic.

3. **Code readability and maintainability**:
   - A variable name describes what the data is for, so you don't have to trace back through literal values when reading the code.

4. **Data transfer**:
   - Variables play an important role in function calls and return values.
   - Through parameters and return values, variables let functions exchange data with each other.

### The evolution of variables

1. **Early programming languages**:
   - In early programming languages (such as assembly and early FORTRAN), variables were used very directly and simply.
   - Variables were often tied straight to memory addresses, and the programmer had to manage their memory by hand.

2. **Procedural programming languages**:
   - With the arrival of procedural languages (such as C and Pascal), variable usage became more abstract.
   - These languages introduced the concepts of local and global variables, supporting scope and lifetime management for variables.

3. **Object-oriented programming languages**:
   - Object-oriented languages (such as C++, Java, and Python) introduced the concepts of instance variables and class variables.
   - Variables can be bound to objects and classes, which ties data and behavior more tightly together.

4. **Functional programming languages**:
   - Functional languages (such as Haskell and Lisp) emphasize immutability: once a variable is assigned, it cannot be changed.
   - This design encourages pure functions and side-effect-free programming, making code more predictable and testable.

5. **Dynamic languages**:
   - Dynamic languages (such as JavaScript, Ruby, and Python) provide dynamically typed variables whose type can change at runtime.
   - That flexibility makes rapid prototyping and scripting easier, but it also brings challenges for type safety.

6. **Modern programming languages**:
   - Modern languages (such as Rust, Go, and Kotlin) have made many improvements to variable management, such as ownership and borrowing (Rust), concurrency safety (Go), and smart type inference (Kotlin).
   - These features improve both the safety and the performance of variable usage.

### Variable types and management

1. **Static and dynamic typing**:
   - Statically typed languages (such as C and Java) determine a variable's type at compile time, giving higher type safety.
   - Dynamically typed languages (such as Python and JavaScript) determine a variable's type at runtime, giving higher flexibility.

2. **Strong and weak typing**:
   - Strongly typed languages strictly restrict operations between different types, avoiding type errors (such as Python and Haskell).
   - Weakly typed languages allow implicit conversions between different types, which can lead to runtime errors (such as JavaScript and PHP).

3. **Scope and lifetime**:
   - Local variables are defined in a function or code block and are valid only within that scope.
   - Global variables are valid for the entire program run, but they can cause naming conflicts and problems that are hard to debug.
   - Static variables are allocated once during program execution, regardless of their scope.

### Variables across programming paradigms

1. **Procedural programming**:
   - Variables hold intermediate results and state during processing.
   - Emphasizes mutating variables and changing state.

2. **Object-oriented programming**:
   - Variables are bound to objects and classes as part of object state.
   - Emphasizes encapsulation and information hiding.

3. **Functional programming**:
   - Variables are usually immutable; once assigned, they cannot be changed.
   - Emphasizes pure functions and side-effect-free programming.

4. **Logical programming**:
   - Variables represent logical variables, which can be bound to values during logical reasoning.
   - Emphasizes binding and unbinding operations on variables.

### Summary

Variables have three common traits: a name, a type (determined at runtime in dynamic languages), and a scope. Whether they are mutable is a paradigm choice — C and Go let you change a value after assignment, while functional languages like Haskell make variables immutable after assignment.

## References

- [Language Spec · Variable declarations](https://go.dev/ref/spec#Variable_declarations)
- [Effective Go · Variables](https://go.dev/doc/effective_go#variables)

## Sibling pages

- [Segment](/var/Segment.md)
- [VarAndInit](/var/VarAndInit.md)
- [Assignment](/var/Assignment.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Segment](/var/Segment.md)
