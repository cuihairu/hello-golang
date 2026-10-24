In Go, local and global variables are placed in different memory regions, and whether they are initialized also affects which segment they land in. Grouped by category here:

###  Memory layout of the program

A program's runtime memory layout typically consists of the following parts:

- **Code segment (Text Segment)**: stores the program's executable instructions and is read-only.
- **Data segment (Data Segment)**: stores initialized global and static variables.
- **BSS segment (Block Started by Symbol)**: stores uninitialized global and static variables.
- **Heap**: used for dynamically allocated memory, typically allocated and freed explicitly by the program.
- **Stack**: used to store the context of function calls, including local variables, function parameters, and return addresses.

### Memory layout diagram

A program's memory layout can be represented with the following diagram:

```
---------------------------
|          Stack          |
|    (local variables)    |
---------------------------
|          Heap           |
|    (dynamic memory)     |
---------------------------
|           BSS           |
| (uninitialized globals) |
---------------------------
|      Data segment       |
|  (initialized globals)  |
---------------------------
|      Code segment       |
|     (program code)      |
---------------------------
```


### Global variables

Global variables (package-level variables) are declared at package level. Their scope is the entire package, and they are allocated memory when the program starts.

#### Initialized global variables

Initialized global variables are allocated memory when the program starts and stored in the data segment. The data segment is the region of memory reserved for the program's static data (including global and static variables).

For example:
```go
package main

var initializedGlobalVar = 42

func main() {
    // ...
}
```

#### Uninitialized global variables

Uninitialized global variables are also allocated memory when the program starts, but they are stored in the BSS segment (Block Started by Symbol), which is reserved for global variables in the program that are not explicitly initialized.

For example:
```go
package main

var uninitializedGlobalVar int

func main() {
    // ...
}
```

### Local variables

Local variables are declared inside a function or code block. Their scope is limited to the function or code block where they are declared.

#### Initialized local variables

Initialized local variables are allocated memory when their function or code block executes and stored on the stack. Stack memory holds temporary data during function calls, including local variables and function parameters. It is characterized by fast allocation and release.

For example:
```go
func exampleFunction() {
    initializedLocalVar := 42
    _ = initializedLocalVar // use it to avoid a compile error
}
```

#### Uninitialized local variables

Uninitialized local variables are also allocated memory when their function or code block executes and stored on the stack. Go automatically gives these variables their zero value.

For example:
```go
func exampleFunction() {
    var uninitializedLocalVar int
    _ = uninitializedLocalVar // use it to avoid a compile error
}
```

### Code example

The four kinds of variable together:

```go
package main

import "fmt"

// initialized global variable
var initializedGlobalVar = 42

// uninitialized global variable
var uninitializedGlobalVar int

func main() {
    // initialized local variable
    initializedLocalVar := 10

    // uninitialized local variable
    var uninitializedLocalVar int

    fmt.Println("Initialized Global Variable:", initializedGlobalVar)
    fmt.Println("Uninitialized Global Variable:", uninitializedGlobalVar)
    fmt.Println("Initialized Local Variable:", initializedLocalVar)
    fmt.Println("Uninitialized Local Variable:", uninitializedLocalVar)
}
```

### Code segment (Code Segment)

The code segment is a region of memory used to store the program's machine code, i.e. its executable instructions. The code segment is read-only, to prevent the program from modifying its own instructions at runtime. Global and local variables are not stored in the code segment; they are stored in the data segment, the BSS segment, or the stack.


### Escape analysis

Local variables live on the stack by default, but the compiler performs escape analysis: when a variable's address is taken out of a function, captured by a closure, or it is too large to stack-allocate, it is moved to the heap and its lifetime is managed by the GC.

```go
package main

import "fmt"

func main() {
    fmt.Println(foo())
}

func foo() *int {
    a := 42
    return &a // a's address escapes the function; a is allocated on the heap
}
```

To tell where a variable actually lands, stack or heap, use `go build -gcflags=-m` to read the compiler's analysis output.

### Summary

- **Global variables**: allocated memory when the program starts; initialized ones go in the data segment, uninitialized ones in the BSS segment.
- **Local variables**: allocated memory when their function or code block executes and stored on the stack; whether or not initialized, uninitialized local variables are given their zero value.
- **Code segment**: stores the program's machine code and is read-only.

Where a variable is declared and whether it is initialized determine whether it lands in the data segment, the BSS segment, or the stack; variables inside a function body ride along with the stack, allocated on entry and reclaimed on exit, which is also why local variables have such a short lifetime.

## References

- [Language Spec · Variable declarations](https://go.dev/ref/spec#Variable_declarations)
- [Effective Go · Variables](https://go.dev/doc/effective_go#variables)
- [Official GC Guide · Escape analysis](https://go.dev/doc/gc-guide#Escape_analysis)
- [Official Blog · Allocating on the Stack](https://go.dev/blog/allocation-optimizations)

## Sibling pages

- [Variable](/var/Variable.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Practice](/zh/alloc/Practice.md)
- [glossary](/zh/glossary.md)
- [Assignment](/var/Assignment.md)
- [ScopeAndLifetime](/var/ScopeAndLifetime.md)
- [Variable](/var/Variable.md)
