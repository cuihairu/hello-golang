In Go, the **receiver operator** is a concept in method definitions, used to specify a method's receiver. The receiver is a special parameter, defined before the method's parameter list, that identifies which type the method belongs to.

### Basic syntax of the receiver operator

```go
func (receiver ReceiverType) MethodName(params) ReturnType {
    // method body
}
```

- **`(receiver ReceiverType)`**: the receiver operator; `receiver` is the receiver variable name of the method, and `ReceiverType` is the receiver's type.
- **`MethodName`**: the method's name.
- **`params`**: the method's parameter list.
- **`ReturnType`**: the method's return type.

### The role of the receiver operator

1. **Specifying the type a method belongs to**: through the receiver operator a method is tied to a particular type, so instance methods of that type can be called.
2. **Implementing object-oriented programming (OOP) concepts**: Go has no traditional classes and inheritance, but methods and receivers give you similar behavior.

### Example code

#### Example 1: Basic use of the receiver operator

```go
package main

import "fmt"

// define a struct type
type Person struct {
    Name string
    Age  int
}

// define a method for the Person type
func (p Person) Greet() {
    fmt.Printf("Hello, my name is %s and I am %d years old.\n", p.Name, p.Age)
}

func main() {
    // create an instance of the Person type
    p := Person{Name: "Alice", Age: 30}
    
    // call the method
    p.Greet() // prints: Hello, my name is Alice and I am 30 years old.
}
```

In this example, `(p Person)` is the receiver operator of the method `Greet`, meaning `Greet` is a method of the `Person` type. `p` is the receiver variable, and its type is `Person`.

#### Example 2: Pointer receiver

Using a pointer as the receiver lets a method modify the receiver's state:

```go
package main

import "fmt"

// define a struct type
type Counter struct {
    Value int
}

// define a method for the Counter type, using a pointer receiver
func (c *Counter) Increment() {
    c.Value++
}

// define another method for the Counter type, using a pointer receiver
func (c *Counter) GetValue() int {
    return c.Value
}

func main() {
    // create an instance of the Counter type
    c := &Counter{Value: 0}
    
    // call the method
    c.Increment()
    fmt.Println("Current value:", c.GetValue()) // prints: Current value: 1
}
```

In this example, `(c *Counter)` is the receiver operator of the methods `Increment` and `GetValue`, meaning these methods belong to the `*Counter` type. Only with a pointer receiver can a method modify the `Value` field of a `Counter` instance.

### Summary

- The **receiver operator** is part of a Go method definition, used to specify the method's receiver type.
- The **receiver** is the method's first parameter, specifying the object the method acts on.
- A **pointer receiver** lets a method modify the receiver's state.
- A **value receiver** gets a copy, so it cannot change the original value and produces no side effects.

Methods attach to types through the receiver operator, which is what lets instances call them in the `p.Greet()` style.

## References

- [Language specification · Operators](https://go.dev/ref/spec#Operators)
- [Language specification · Address operators](https://go.dev/ref/spec#Address_operators)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Operator](/operator/Operator.md)
- [Relational](/operator/Relational.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Operator](/operator/Operator.md)
- [Relational](/operator/Relational.md)
