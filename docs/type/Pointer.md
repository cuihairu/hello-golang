In Go, a pointer type holds the memory address of a variable. You use it when passing large structs, or when a function needs to modify the caller's variable.

### 1. Declaring Pointer Types

A pointer type declaration uses the `*` symbol. For example, `*int` represents a pointer to an `int` type.

```go
var p *int
```

### 2. Getting the Address of a Variable

Use the `&` symbol to get the address of a variable.

```go
package main

import "fmt"

func main() {
    var x int = 10
    p := &x
    fmt.Println(p) // prints: the memory address of variable x, e.g. 0xc0000140a0
}
```

### 3. Accessing and Modifying a Variable's Value Through a Pointer

Use the `*` symbol to access the value of the variable a pointer points to, and also to modify the variable's value through the pointer.

```go
package main

import "fmt"

func main() {
    var x int = 10
    p := &x

    // access the value the pointer points to
    fmt.Println(*p) // prints: 10

    // modify the value through the pointer
    *p = 20
    fmt.Println(x) // prints: 20
}
```

### 4. Use Cases for Pointers

#### Function Argument Passing

In Go, function arguments are passed by value, which means the function receives a copy of the argument. By passing a pointer, the function can operate directly on the original variable.

```go
func increment(p *int) {
    *p++
}

func main() {
    x := 10
    increment(&x)
    fmt.Println(x) // prints: 11
}
```

#### Struct Fields

Pointers are often used for struct fields to avoid copying the entire struct when passing it as a function argument, which improves efficiency.

```go
type Person struct {
    Name string
    Age  int
}

func updatePerson(p *Person) {
    p.Name = "Alice"
    p.Age = 30
}

func main() {
    person := Person{Name: "Bob", Age: 25}
    updatePerson(&person)
    fmt.Println(person) // prints: {Alice 30}
}
```

#### Dynamic Memory Allocation

Use the `new` function to dynamically allocate memory and get back a pointer to that memory.

```go
p := new(int)
*p = 100
fmt.Println(*p) // prints: 100
```

### 5. Safety and Limitations of Pointers

#### No Pointer Arithmetic

Unlike C and C++, Go does not support pointer arithmetic (such as adding or subtracting from a pointer). This makes programs safer and avoids many common mistakes.

#### Automatic Garbage Collection

Go has an automatic garbage collection mechanism, so programmers do not have to manage memory manually. This greatly simplifies the use of pointers and reduces the likelihood of memory leaks and dangling pointers.

### Example Code

This example strings together declaration, address-taking, dereferencing, `new`, and modifying a struct:

```go
package main

import "fmt"

func main() {
    var x int = 10
    var p *int = &x
    
    fmt.Println("Address of x:", p)  // prints: the memory address of x, e.g. 0xc0000140a0
    fmt.Println("Value of x:", *p)   // prints: 10
    
    *p = 20
    fmt.Println("New value of x:", x) // prints: 20
    
    // modify a variable's value using a function
    increment := func(p *int) {
        *p++
    }

    increment(&x)
    fmt.Println("Incremented value of x:", x) // prints: 21
    
    // dynamic memory allocation
    ptr := new(int)
    *ptr = 100
    fmt.Println("Value of ptr:", *ptr) // prints: 100
    
    // pointer as a struct field
    type Person struct {
        Name string
        Age  int
    }
    
    modifyPerson := func(p *Person) {
        p.Name = "Alice"
        p.Age = 30
    }

    person := Person{Name: "Bob", Age: 25}
    modifyPerson(&person)
    fmt.Println("Modified person:", person) // prints: {Alice 30}
}
```

### Summary

`&` takes an address, `*` dereferences, and `new` allocates memory and returns a pointer. Beyond those three symbols, Go's pointers keep one key difference from C: no pointer arithmetic. Combined with automatic garbage collection, problems like dangling pointers drop by a large margin.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Pointer types](https://go.dev/ref/spec#Pointer_types)
- [Effective Go · Pointers vs values](https://go.dev/doc/effective_go#pointers_vs_values)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Ring](/type/Ring.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Ring](/type/Ring.md)
