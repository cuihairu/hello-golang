### Interfaces and reflection in Go, explained


> Perspective: this article focuses on an interface's runtime representation and its relationship with reflection; for interface definitions and how to implement them, see [OOP notes](/zh/oop/Interface.md).
Go interfaces hold any concrete type that implements the interface's methods at runtime, using two underlying fields, `itab` and `data`. Reflection lets a program inspect and manipulate an interface's type and value at runtime. Below I go from the basic syntax to the structure of `iface` and `itab`, then cover polymorphism, duck typing, and how reflection ties in.

### Basic interface syntax

In Go, an interface type defines a set of methods without providing the implementations. Any type that implements those methods is considered to implement the interface.

```go
package main

import "fmt"

type Speaker interface {
    Speak() string
}

type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

func main() {
    var s Speaker
    s = Dog{}
    fmt.Println(s.Speak()) // prints "Woof!"
}
```

### The underlying implementation of interfaces

In Go, an interface variable is actually a tuple containing both a type and a value. Specifically, an interface variable has two parts:

1. **`type`**: holds metadata about the actual type.
2. **`value`**: holds the value of the concrete type.

This implementation represents an interface variable with two fields:

```go
type iface struct {
    tab  *itab
    data unsafe.Pointer
}

type itab struct {
    inter *interfacetype
    _type *_type
    hash  uint32
    _     [4]byte
    fun   [1]uintptr
}
```

- **`iface`**: represents a generic interface variable.
  - `tab`: points to an `itab` struct that holds type information.
  - `data`: points to the actual data.
- **`itab`**: represents the concrete implementation of an interface type.
  - `inter`: points to the interface type's information.
  - `_type`: points to the concrete type's information.
  - `fun`: holds an array of function pointers for the interface's methods.

When a value is assigned to an interface variable, Go creates an `itab` and stores the pointer to the actual data in the interface variable's `data` field.

### Polymorphism with interfaces

Interfaces implement polymorphism, so the same interface type can represent different concrete types. For example, several different types can implement the same interface, and then they can be stored in and called through the same interface variable.

```go
package main

import "fmt"

type Speaker interface {
    Speak() string
}

type Dog struct{}
type Cat struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

func (c Cat) Speak() string {
    return "Meow!"
}

func main() {
    var s Speaker
    s = Dog{}
    fmt.Println(s.Speak()) // prints "Woof!"
    s = Cat{}
    fmt.Println(s.Speak()) // prints "Meow!"
}
```

### Inheritance with interfaces

Interfaces can achieve inheritance by nesting other interfaces. For example, one interface can contain all the methods of another interface.

```go
package main

import "fmt"

type Speaker interface {
    Speak() string
}

type Animal interface {
    Speaker
    Move() string
}

type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

func (d Dog) Move() string {
    return "Run"
}

func main() {
    var a Animal = Dog{}
    fmt.Println(a.Speak()) // prints "Woof!"
    fmt.Println(a.Move())  // prints "Run"
}
```

### Interface polymorphism and type assertions

A type assertion converts an interface type into a concrete type, so you can call the concrete type's methods.

```go
package main

import "fmt"

type Speaker interface {
    Speak() string
}

type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

func main() {
    var s Speaker = Dog{}
    if d, ok := s.(Dog); ok {
        fmt.Println(d.Speak()) // prints "Woof!"
    }
}
```

### Comparison with interfaces in traditional languages

Compared with traditional languages like Java, Go interfaces differ in several significant ways:

1. **Implicit implementation**: in Go, a type doesn't need to explicitly declare that it implements an interface; it just has to implement all the methods the interface defines.
2. **Duck typing**: as long as an object implements the methods an interface requires, it can be assigned to an interface variable, with no prior declaration.
3. **Interface composition**: Go interfaces can build more complex interface types by composing other interfaces.

### Duck typing

Duck typing is a form of dynamic typing: as long as an object implements the methods an interface needs, it can be treated as an implementation of that interface type.

```go
package main

import "fmt"

type Speaker interface {
    Speak() string
}

type Dog struct{}
type Robot struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

func (r Robot) Speak() string {
    return "Beep Boop"
}

func main() {
    var s Speaker

    s = Dog{}
    fmt.Println(s.Speak()) // prints "Woof!"

    s = Robot{}
    fmt.Println(s.Speak()) // prints "Beep Boop"
}
```

### Comparison with Rust traits

Traits in Rust are similar to Go interfaces, but there are some differences:

1. **Explicit declaration**: in Rust, you have to explicitly declare that a type implements a given trait.
2. **Generic support**: Rust traits can act as generic constraints, and since Go 1.18 interfaces can play a similar role.
3. **Static dispatch**: Rust traits use static dispatch, while Go interfaces use dynamic dispatch. This means Rust determines the call at compile time, whereas Go determines it at runtime.

### Pros, cons, and usage notes

#### Pros

1. **Polymorphism**: different types implementing the same interface can be used interchangeably.
2. **Decoupling**: the caller depends on the interface rather than the concrete type, so swapping in a new implementation doesn't require changes at the call site.

#### Cons

1. **Runtime overhead**: interface calls are dynamically dispatched, which can carry some performance cost.
2. **Type safety**: type assertions happen at runtime and can cause runtime errors.

#### Usage notes

1. **Keep interfaces small**: when designing interfaces, keep them small and simple, with only the methods you actually need.
2. **Avoid overusing reflection**: reflection adds runtime overhead and tends to push errors out to runtime, so before reaching for it, make sure there's no other way to write it.

### The relationship between interfaces and reflection

Go's reflection mechanism lets a program inspect and manipulate interface types and values at runtime. This is especially useful for interfaces, because an interface variable can hold any value that implements its methods at runtime.

#### Inspecting interface types and values with reflection

The `reflect` package provides a set of functions for inspecting and manipulating interface variables; the most common are `reflect.TypeOf` and `reflect.ValueOf`.

```go
package main

import (
    "fmt"
    "reflect"
)

type Speaker interface {
    Speak() string
}

type Dog struct{}

func (d Dog) Speak() string {
    return "Woof!"
}

func main() {
    var s Speaker = Dog{}

    // inspect the interface's type and value with reflection
    t := reflect.TypeOf(s)
    v := reflect.ValueOf(s)

    fmt.Println("Type:", t)
    fmt.Println("Value:", v)

    // inspect the concrete type and value underneath the interface
    fmt.Println("Underlying Type:", v.Type())
    fmt.Println("Underlying Value:", v.Interface())
}
```

#### Modifying interface values with reflection

Reflection also lets you modify an interface variable's value at runtime.

```go
package main

import (
    "fmt"
    "reflect"
)

type Speaker interface {
    Speak() string
}

type Dog struct {
    Sound string
}

func (d Dog) Speak() string {
    return d.Sound
}

func main() {
    var s Speaker = &Dog{Sound: "Woof!"}

    v := reflect.ValueOf(s).Elem()

    // modify the concrete value underneath the interface
    field := v.FieldByName("Sound")
    if field.CanSet() && field.Kind() == reflect.String {
        field.SetString("Bark!")
    }

    fmt.Println(s.Speak()) // prints "Bark!"
}
```

#### Limitations of reflection

Reflection's power comes at the cost of runtime inspection, mainly in three ways:

1. **Performance overhead**: reflection operations are usually slower than direct ones, because they involve dynamic type checks and method calls.
2. **Safety**: reflection makes it easy to introduce runtime errors, such as trying to modify a field that can't be modified.
3. **Readability**: code that uses reflection is usually harder to understand and maintain.

### Summary

An interface variable is made of `itab` and `data`: the former is the method table linking the interface and the concrete type, the latter points at the data. Type assertions and reflection both read this same structure. Keep interfaces small when you write code, and reach for reflection only when there's nothing else.

## References

- [Language Spec · Types](https://go.dev/ref/spec#Types)
- [Language Spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Interfaces](https://go.dev/doc/effective_go#interfaces)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/zh/glossary.md)
- [Array](/type/Array.md)
- [BaseConv](/type/BaseConv.md)
- [Big](/type/Big.md)
- [Bool](/type/Bool.md)
- [Byte](/type/Byte.md)
- [Complex](/type/Complex.md)
- [CompositeType](/type/CompositeType.md)
- [Conv](/type/Conv.md)
- [Float](/type/Float.md)
- [HtmlTemplate](/type/HtmlTemplate.md)
- [Int](/type/Int.md)
- [Json](/type/Json.md)
- [LinkedList](/type/LinkedList.md)
- [Pointer](/type/Pointer.md)
- [Ring](/type/Ring.md)
- [Rune](/type/Rune.md)
- [String](/type/String.md)
- [Struct](/type/Struct.md)
- [Template](/type/Template.md)
- [Type](/type/Type.md)
