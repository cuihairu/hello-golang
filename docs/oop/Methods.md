# Method Declarations
In Go, a method is a function associated with a particular type, and it can be attached to a struct type or a custom type.

### 1. Defining Methods

The syntax for defining a method is as follows:

```go
func (receiver ReceiverType) MethodName(params) ReturnType {
    // method body
}
```

- **receiver**: the receiver variable, indicating which type's value the method acts on.
- **ReceiverType**: the type of the receiver.
- **MethodName**: the method name.
- **params**: the list of parameters.
- **ReturnType**: the return type.

#### Example: Basic method definition

```go
package main

import "fmt"

type Circle struct {
    Radius float64
}

// define the method
func (c Circle) Area() float64 {
    return 3.14 * c.Radius * c.Radius
}

func main() {
    circle := Circle{Radius: 5}
    fmt.Println("Area:", circle.Area()) // prints: Area: 78.5
}
```

### 2. Method Receivers

A method's receiver can be a value type or a pointer type.

- **Value receiver**: the method's receiver is a copy of the type. The method cannot modify the original value.
- **Pointer receiver**: the method's receiver is a pointer to the type. The method can modify the original value.

#### Example: Value receiver vs pointer receiver

```go
package main

import "fmt"

type Rectangle struct {
    Width, Height int
}

// value receiver: the method cannot modify the Rectangle instance
func (r Rectangle) Area() int {
    return r.Width * r.Height
}

// pointer receiver: the method can modify the Rectangle instance
func (r *Rectangle) Scale(factor int) {
    r.Width *= factor
    r.Height *= factor
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}
    fmt.Println("Area:", rect.Area()) // prints: Area: 50

    rect.Scale(2)
    fmt.Println("Scaled Width:", rect.Width)  // prints: Scaled Width: 20
    fmt.Println("Scaled Height:", rect.Height) // prints: Scaled Height: 10
}
```

### 3. Methods and Custom Types

Go allows you to define methods for custom types. These custom types can be aliases of basic types or aliases of structs.

#### Example: Methods on a custom type

```go
package main

import "fmt"

// custom type
type MyInt int

// method of the custom type
func (n MyInt) Double() MyInt {
    return n * 2
}

func main() {
    num := MyInt(10)
    fmt.Println("Double:", num.Double()) // prints: Double: 20
}
```

### 4. Methods and Interfaces

Methods can be used in interfaces. An interface defines a set of methods, and any type that implements those methods can be considered to implement that interface.

#### Example: Methods in an interface

```go
package main

import "fmt"

// define the interface
type Speaker interface {
    Speak() string
}

// types that implement the interface
type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

type Cat struct{}

func (c Cat) Speak() string {
    return "Meow!"
}

func main() {
    var speaker Speaker

    speaker = Dog{}
    fmt.Println(speaker.Speak()) // prints: Woof!

    speaker = Cat{}
    fmt.Println(speaker.Speak()) // prints: Meow!
}
```

### 5. Method Receiver Types

- **Value receiver**: the method operates on a copy of the receiver and cannot modify the original value; use it when the receiver object is small and the receiver's state does not need to change.
- **Pointer receiver**: use it for methods that need to modify the receiver's value, or when the receiver object is large, to avoid copying the whole object on every call.

### 6. Method Nesting

Go supports inheritance-like behavior through embedding. Embedding lets one struct contain another, so it inherits that struct's fields and methods.

#### Example: Embedded structs

```go
package main

import "fmt"

// base struct
type Animal struct {
    Name string
}

func (a Animal) Speak() string {
    return "Some generic sound"
}

// the struct that embeds Animal
type Dog struct {
    Animal
    Breed string
}

func main() {
    dog := Dog{Animal: Animal{Name: "Buddy"}, Breed: "Golden Retriever"}
    fmt.Println(dog.Name)  // prints: Buddy
    fmt.Println(dog.Speak()) // prints: Some generic sound
}
```

### Summary

- **Method definition**: define a function associated with a particular type through a receiver type and a method name.
- **Receiver type**: can be a value type or a pointer type, which determines whether the method can modify the original value.
- **Methods on custom types**: you can define methods for custom types of basic types or structs.
- **Methods in interfaces**: an interface defines a set of methods, and a type satisfies the interface by implementing those methods.
- **Method embedding**: achieve inheritance-like behavior through struct embedding.

Whether a receiver is a value or a pointer decides whether the method can modify the original value, and whether each call copies the receiver.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
- [Language spec · Method declarations](https://go.dev/ref/spec#Method_declarations)


## Sibling pages

- [Embedding](/oop/Embedding.md)
- [Interface](/oop/Interface.md)
- [PointerReceiver](/oop/PointerReceiver.md)
- [InterfaceImpl](/oop/InterfaceImpl.md)
- [OOP](/oop/OOP.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [InterfaceImpl](/oop/InterfaceImpl.md)
- [OOP](/oop/OOP.md)
