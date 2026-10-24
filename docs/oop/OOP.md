Object-oriented programming (OOP) is a programming paradigm that organizes code around objects and classes. Go has no traditional classes or inheritance; structs, methods, interfaces, and embedding together cover the core features of OOP.

### Basic Concepts of Object-Oriented Programming (OOP)

1. **Class**: a class is the blueprint of an object, defining the object's attributes and behaviors. In traditional object-oriented languages, a class contains fields (attributes) and methods (behaviors).

2. **Object**: an object is an instance of a class, containing the attributes and methods defined by the class.

3. **Inheritance**: inheritance allows one class to inherit another class's attributes and methods, achieving code reuse.

4. **Encapsulation**: encapsulation bundles data and the methods that operate on it together, hiding internal implementation details and exposing only the necessary interface.

5. **Polymorphism**: polymorphism allows objects to express their behavior in different ways, typically implemented through references to an interface or a base class.

### Object-Oriented Programming in Go

Go has no classes and no inheritance mechanism. Structs plus methods take on similar roles:

#### 1. Structs

Go uses structs to define data types, similar to classes in traditional object-oriented languages.

```go
package main

import "fmt"

// define the struct
type Person struct {
    Name string
    Age  int
}

func main() {
    // create a struct instance
    p := Person{Name: "Alice", Age: 30}
    fmt.Println(p.Name, p.Age) // prints: Alice 30
}
```

#### 2. Methods

A method is a function associated with a struct type. Defining a method is similar to defining a regular function, except that it has a receiver, which is the struct instance the method operates on.

```go
package main

import "fmt"

// define the struct
type Rectangle struct {
    Width, Height int
}

// define the method
func (r Rectangle) Area() int {
    return r.Width * r.Height
}

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

#### 3. Interfaces

An interface in Go defines a set of methods. A type satisfies the interface by implementing those methods. Interfaces allow polymorphism.

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

#### 4. Embedding

Go supports inheritance-like behavior through struct embedding. Embedding lets one struct contain another, so it inherits that struct's fields and methods.

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

- **Classes and objects**: Go uses structs to encapsulate and organize data. A struct is like a traditional class.
- **Methods**: Go uses methods to define behavior associated with a struct, like member methods in a class.
- **Interfaces**: interfaces let Go achieve polymorphism. A type satisfies an interface by implementing its methods.
- **Embedding**: Go supports inheritance-like behavior through struct embedding, letting one struct contain another's fields and methods.

Put these four together and Go gets encapsulation (visibility controlled by capitalization), reuse (embedding), and polymorphism (interfaces). The price is no inheritance hierarchy: all relationships between types are expressed through composition.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)


## Sibling pages

- [Embedding](/oop/Embedding.md)
- [Interface](/oop/Interface.md)
- [PointerReceiver](/oop/PointerReceiver.md)
- [Methods](/oop/Methods.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Methods](/oop/Methods.md)
