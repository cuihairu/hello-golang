
> Perspective: this page covers interface definition and implementation from the angle of types and object-oriented concepts; for the runtime representation of an interface and its connection to reflection, see [Interface and reflection notes](/type/Interface.md).
In Go, interfaces and types are two fundamental concepts: a type describes what data looks like, an interface describes what an object can do.

### 1. Types in Go (Type)

#### Definition

A type is a basic building block in Go. It defines the form of data such as variables, constants, structs, and arrays. In Go, types are used to declare variables and create structures.

**Example: Basic type definition**

```go
type Age int
type Name string

var myAge Age
var myName Name
```

#### Usage

Types are used to create variables and struct fields, to define function parameters and return values, and to implement methods. You can define new data types with types, which makes code more self-documenting and structured.

**Example: Struct type**

```go
type Person struct {
    Name string
    Age  int
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    fmt.Println(p.Name, p.Age)
}
```

### 2. Interfaces in Go (Interface)

#### Definition

An interface is an abstract type that defines a set of methods. Any type that implements all the methods defined in the interface is considered to implement that interface. The purpose of an interface is to let the same piece of code handle objects of different types.

**Example: Interface definition**

```go
type Speaker interface {
    Speak() string
}
```

#### Usage

Interfaces are used to define a set of methods so that different types can achieve polymorphism by implementing the same interface. The implementation of an interface method does not need to live in the same type as the interface definition, which allows different types to implement an interface without modifying it.

**Example: Interface implementation**

```go
type Speaker interface {
    Speak() string
}

type Person struct {
    Name string
}

func (p Person) Speak() string {
    return "Hi, I'm " + p.Name
}

func greet(s Speaker) {
    fmt.Println(s.Speak())
}

func main() {
    p := Person{Name: "Alice"}
    greet(p) // prints: Hi, I'm Alice
}
```

### 3. Differences and Relationship

#### Differences between types and interfaces

1. **Definition and purpose**:
   - **Types**: used to define the concrete form and structure of data, such as structs, arrays, and slices. They describe how data is stored and operated on.
   - **Interfaces**: define a set of methods without caring about their concrete implementation. An interface provides an abstraction mechanism that lets different types be interchangeable by implementing the same methods.

2. **How they're implemented**:
   - **Types**: define how data is stored and operated on. Different types have different fields and methods.
   - **Interfaces**: only define method signatures, without providing implementations. Any type that implements all the methods in an interface implements that interface.

3. **Use**:
   - **Types**: organize data and implement operations on it.
   - **Interfaces**: describe behavioral contracts, so different types can be handled uniformly by the same set of method signatures.

#### The relationship between types and interfaces

- **Types implement interfaces**: a type can implement one or more interfaces. The implementation of interface methods is provided by the concrete type.
- **Interface types**: an interface is itself a kind of type, but it does not store concrete data. It is used to describe an object's behavior.
- **Polymorphism**: interfaces allow objects of different types to be operated on through the same interface, achieving polymorphism.

### 4. Example: Using Types and Interfaces Together

**Example: A type implementing an interface**

```go
package main

import "fmt"

// define the interface
type Formatter interface {
    Format() string
}

// define the type
type Person struct {
    Name string
}

// implement the interface method
func (p Person) Format() string {
    return "Name: " + p.Name
}

func printFormatted(f Formatter) {
    fmt.Println(f.Format())
}

func main() {
    p := Person{Name: "Bob"}
    printFormatted(p) // prints: Name: Bob
}
```

### Summary

- **Types (Type)**: define how data is stored and operated on.
- **Interfaces (Interface)**: define a set of method signatures that describe a behavioral contract.

Once a type implements all of an interface's methods, it can be assigned to an interface variable; a function parameter typed as an interface accepts any type that implements those methods. That is how Go achieves polymorphism.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [InterfaceImpl](/oop/InterfaceImpl.md)
- [Methods](/oop/Methods.md)
- [OOP](/oop/OOP.md)
- [Poly](/oop/Poly.md)
