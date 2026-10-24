In computer science, a programming type (or type system) is a classification system used to constrain and manage the data and expressions in a program. It defines how data is represented, which operations are allowed, and the rules for interpreting those operations. Type systems are one of the core concepts of a programming language, directly affecting code readability and reliability.

### The Nature and Function of Type Systems

1. **Data Representation and Storage**:
   - **Primitive Types**: integers, floating-point numbers, booleans, and so on, define how basic data is stored and operated on.
   - **Composite Types**: arrays, structs, functions, and so on, combine multiple pieces of data into a single unit and define how those units are accessed and operated on.

2. **Operations and Syntax Rules**:
   - **Type Checking**: the compiler or interpreter checks type consistency at compile time or run time, preventing illegal operations between different types.
   - **Type Conversion**: allows converting a value of one type into another, usually in two forms: implicit and explicit.
   - **Type Inference**: some languages can infer the type of an expression from context, reducing redundant type declarations.

3. **Programming Style and Constraints**:
   - **Static vs Dynamic Types**: statically typed languages check types at compile time, dynamically typed languages check them at run time.
   - **Strong vs Weak Types**: strongly typed languages require strict type conversion, weakly typed languages are more flexible and allow implicit conversion.

4. **Safety and Reliability**:
   - Type systems help prevent many common programming errors, such as null pointer references and mismatched type operations.
   - Strongly and statically typed languages usually offer higher safety and reliability, because the compiler catches many potential issues at compile time.

5. **Abstraction and Modularity**:
   - Type systems support data abstraction and modular design; by defining custom types and interfaces, implementation details can be separated from data structures.

### Example: Comparing the Type Systems of C and Python

- **C**: statically typed, strongly typed, requires explicit variable type declarations, and the compiler checks types at compile time.

  ```c
  int x = 10;
  float y = 3.14;
  ```

- **Python**: dynamically typed, strongly typed, a variable's type is determined at run time, but variables must be defined before use.

  ```python
  x = 10
  y = 3.14
  ```

### Declaring Types with `type`: Definition vs Alias

The `type` keyword has two forms, distinguished by the presence or absence of `=`.

`type MyString string` defines a new type whose underlying type is `string`, but the two are different types; assigning between them requires an explicit conversion, and the new type can have its own methods:

```go
package main

import "fmt"

type MyString string

func (m MyString) Hello() string {
    return "Hello, " + string(m)
}

func main() {
    var s MyString = "Go"
    fmt.Println(s.Hello())

    var str string = string(s) // requires explicit conversion
    fmt.Println(str)
}
```

`type MyString2 = string` is a type alias; `MyString2` and `string` are the same type, so you can assign directly without conversion:

```go
package main

import "fmt"

type MyString2 = string

func main() {
    var s MyString2 = "Hello, Go"
    var str string = s // same type, no conversion needed
    fmt.Println(str)
}
```

`type` can also declare structs, interfaces, and function types, corresponding to `type Person struct{...}`, `type Describer interface{...}`, and `type MathOperation func(int, int) int` respectively. See the structs, interfaces, and functions chapters for the details.

### Summary

A programming type defines the structure and operations of data and is the foundation of a programming language. Whether static or dynamic, strong or weak, the different combinations determine whether errors surface at compile time or run time, and they also shape how you write code.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Template](/type/Template.md)
- [TypeInference](/type/TypeInference.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Template](/type/Template.md)
