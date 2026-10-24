Go has no inheritance in the traditional object-oriented sense. Struct embedding is Go's approach: embed one struct anonymously into another, and its fields and methods become directly reusable.

### 1. Defining Embedded Structs

An embedded struct is one struct defined as a field of another struct. This lets the outer struct access the embedded struct's fields and methods directly.

#### Example: Basic embedded struct

```go
package main

import "fmt"

// basic struct
type Person struct {
    Name string
    Age  int
}

// another struct that embeds Person
type Employee struct {
    Person      // embedded struct
    EmployeeID string
}

func main() {
    e := Employee{
        Person:      Person{Name: "Alice", Age: 30},
        EmployeeID: "E123",
    }
    fmt.Println("Name:", e.Name)         // access the field through the embedded struct
    fmt.Println("Age:", e.Age)           // access the field through the embedded struct
    fmt.Println("Employee ID:", e.EmployeeID)
}
```

### 2. Advantages of Embedding Structs

#### 1. Code reuse

Write fields and methods once, and any struct that embeds it can use them directly — no copy-paste.

#### 2. Simpler design

Keep common functionality in one struct, and other structs can embed it to get those features.

#### 3. Inheritance-like

Go has no inheritance. When you need to reuse fields and methods, embedding is the closest thing.

### 3. Accessing Embedded Struct Fields and Methods

The embedded struct's fields and methods can be accessed directly, as if they were part of the outer struct.

#### Example: Accessing embedded struct fields and methods

```go
package main

import "fmt"

type Address struct {
    Street, City, State string
}

type Person struct {
    Name    string
    Address // embedded struct
}

func main() {
    p := Person{
        Name: "Bob",
        Address: Address{
            Street: "123 Main St",
            City:   "Springfield",
            State:  "IL",
        },
    }
    fmt.Println("Name:", p.Name)
    fmt.Println("Street:", p.Street) // access the embedded struct's field directly
    fmt.Println("City:", p.City)
    fmt.Println("State:", p.State)
}
```

### 4. Methods and Embedded Structs

When methods are defined in an embedded struct, the outer struct can call them directly.

#### Example: Methods in an embedded struct

```go
package main

import "fmt"

type Person struct {
    Name string
}

func (p Person) Greet() string {
    return "Hello, " + p.Name
}

type Employee struct {
    Person
    EmployeeID string
}

func main() {
    e := Employee{
        Person:      Person{Name: "Charlie"},
        EmployeeID: "E456",
    }
    fmt.Println(e.Greet()) // call the embedded struct's method directly
}
```

### 5. Method Redeclaration

If the outer struct and the embedded struct both have a method with the same name, the outer struct's method overrides the embedded one. You can explicitly access the shadowed method using the embedded struct's type name.

#### Example: Method redeclaration

```go
package main

import "fmt"

type Base struct{}

func (b Base) Do() {
    fmt.Println("Base Do")
}

type Derived struct {
    Base
}

func (d Derived) Do() {
    fmt.Println("Derived Do")
}

func main() {
    d := Derived{}
    d.Do()          // prints: Derived Do
    d.Base.Do()     // prints: Base Do
}
```

### 6. Multiple Embedded Structs

A struct can embed multiple structs, combining the functionality of several of them.

#### Example: Multiple embedding

```go
package main

import "fmt"

type Address struct {
    Street string
}

type ContactInfo struct {
    Email string
}

type Person struct {
    Address     // embedded struct
    ContactInfo // embedded struct
    Name        string
}

func main() {
    p := Person{
        Address:     Address{Street: "456 Elm St"},
        ContactInfo: ContactInfo{Email: "bob@example.com"},
        Name:        "Bob",
    }
    fmt.Println("Name:", p.Name)
    fmt.Println("Street:", p.Street)
    fmt.Println("Email:", p.Email)
}
```

### 7. Anonymous Fields

In Go, the fields of an embedded struct are anonymous — you don't give the embedded struct field a name. This lets the embedded struct's fields be accessed directly.

#### Example: Anonymous fields

```go
package main

import "fmt"

type Engine struct {
    Horsepower int
}

type Car struct {
    Engine     // anonymous embedding
    Model string
}

func main() {
    c := Car{
        Engine: Engine{Horsepower: 150},
        Model:  "Toyota Camry",
    }
    fmt.Println("Model:", c.Model)
    fmt.Println("Horsepower:", c.Horsepower) // access the anonymous field's field directly
}
```

### Summary

Embedding promotes the inner struct's fields and methods into the outer struct's namespace: write `e.Name` instead of `e.Person.Name`. When names collide, the outer one shadows the inner one; to call the inner one, use the fully qualified form like `d.Base.Do()`.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
- [Language spec · Struct types (embedded fields)](https://go.dev/ref/spec#Struct_types)

## Sibling pages

- [Poly](/oop/Poly.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [InterfaceImpl](/oop/InterfaceImpl.md)
- [Methods](/oop/Methods.md)
- [OOP](/oop/OOP.md)
- [Poly](/oop/Poly.md)
