### History and standards of functions

The concept of a function comes from early mathematics and logic. In computer science it is the basic unit for abstracting and organizing code, and the development of programming languages has always revolved around it.

#### Early development

1. **Lambda calculus**: introduced by Alonzo Church in the 1930s, it is a formal system for defining function abstraction and application. Lambda calculus had a profound influence on functional programming languages.

2. **Fortran**: released in 1957, Fortran (Formula Translation) was the first widely used high-level programming language. Fortran introduced the concepts of subroutine and function, used for code reuse and modularity.

3. **ALGOL**: released in 1958, ALGOL (Algorithmic Language) further developed the concept of the function, introducing block structure and recursive functions. ALGOL had a profound influence on the design of modern programming languages such as Pascal and C.

4. **LISP**: developed by John McCarthy in 1958, LISP (LISt Processing) was one of the earliest functional programming languages, emphasizing functions as first-class citizens that can be passed as arguments and returned.

#### Standardization and specifications

Standardization was driven by various standards bodies and language designers; a few key standards and specifications:

1. **C language standard (ANSI C and ISO C)**: the standardization of C was carried out by the American National Standards Institute (ANSI) and the International Organization for Standardization (ISO), which published the ANSI C (1989) and ISO C (1990) standards, defining the syntax and calling conventions of functions.

2. **POSIX standard**: the POSIX (Portable Operating System Interface) standard defines the UNIX operating system interface, including the specifications and calling conventions for standard library functions.

3. **IEEE standard**: the IEEE 754 standard defines floating-point arithmetic and its use within functions.

4. **ISO standards for programming languages**: for example ISO/IEC 14882 (the C++ standard), ISO/IEC 9899 (the C standard), ISO/IEC 9126 (software quality model). These standards define the syntax, semantics, and library function behavior of a language.

### Function calling conventions

Calling conventions define how arguments are passed, how return values are carried back, and how the caller and callee cooperate. They differ by language, compiler, and platform; common ones include:

1. **cdecl (C Declaration)**:
   - Arguments are pushed onto the stack from right to left.
   - The caller is responsible for cleaning up the stack.
   - The return value is returned via a register (usually `EAX` or `RAX`).

2. **stdcall (Standard Call)**:
   - Arguments are pushed onto the stack from right to left.
   - The callee is responsible for cleaning up the stack.
   - Commonly used for Windows API functions.

3. **fastcall (Fast Call)**:
   - The first two arguments are passed via registers, the rest via the stack.
   - The caller or the callee cleans up the stack (depending on the implementation).

4. **thiscall**:
   - Used exclusively for C++ member functions.
   - The `this` pointer is passed via a register, the rest of the arguments follow cdecl or stdcall.

5. **vectorcall**:
   - Arguments are passed via registers (including vector registers) to improve performance.
   - The caller or the callee cleans up the stack (depending on the implementation).

### The evolution of functions and modern features

Functions have kept growing in shape, and modern languages add these features:

1. **Anonymous functions and lambda expressions**:
   - Many modern languages (such as C++11, Java 8, Python, JavaScript) have introduced anonymous functions and lambda expressions, allowing short functions to be defined and used on the fly.

2. **Higher-order functions**:
   - Functions can be passed as arguments to other functions, or returned from other functions. This is especially important in functional programming, such as in Haskell and Scala.

3. **Closures**:
   - A function can capture and remember the environment variables in scope when it was defined, and can still access them even after that environment has left its scope. This is very common in languages such as JavaScript, Python, and Go.

4. **Coroutines**:
   - A coroutine is a control-flow mechanism more advanced than a traditional function, allowing a function to suspend and resume during execution. Python, Lua, and Kotlin all support coroutines.

5. **Generic functions**:
   - Allow type parameters in a function definition so that the function can handle multiple data types. For example, template functions in C++ and generic methods in Java.

### Example: lambda expressions and higher-order functions in modern C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> numbers = {1, 2, 3, 4, 5};

    // define an anonymous function using a lambda expression
    auto square = [](int x) { return x * x; };

    // use the higher-order function std::transform to apply the lambda expression
    std::transform(numbers.begin(), numbers.end(), numbers.begin(), square);

    // print the result
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

This example shows how to use lambda expressions and higher-order functions in C++, applying an anonymous function to each element of a vector through the `std::transform` function.

From lambda calculus in the 1930s, to subroutines in Fortran and first-class functions in LISP, to closures and generic functions today, the function has grown into what it is now. Standards such as ANSI C and POSIX pin down how calls work and how library functions behave, so that code stays aligned across platforms and languages.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Official FAQ](https://go.dev/doc/faq)


## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [FuncValue](/func/FuncValue.md)
- [InnerFunc](/func/InnerFunc.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FuncValue](/func/FuncValue.md)
- [InnerFunc](/func/InnerFunc.md)
