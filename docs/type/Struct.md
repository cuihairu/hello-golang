## `struct` in Go, explained

A `struct` in Go is an aggregate data type that groups multiple values together, which can be of different types. It's the equivalent of classes or records in other programming languages.

### 1. Basic `struct` syntax

The basic syntax for defining a `struct` and creating instances is as follows:

```go
// define a struct
type Person struct {
    Name string
    Age  int
}

// create instances
func main() {
    // initialize using field names
    p1 := Person{Name: "Alice", Age: 30}
    
    // initialize in order
    p2 := Person{"Bob", 25}
    
    // zero-value initialization
    var p3 Person

    // access and modify fields
    p1.Name = "Charlie"
    fmt.Println(p1.Name, p1.Age)
    fmt.Println(p2) // prints {Bob 25}
    fmt.Println(p3) // prints { 0} (zero value)
}
```

### 2. `struct` memory usage and the empty `struct`

A `struct`'s memory footprint depends on its field types and alignment. An empty `struct{}` takes up no space at all (size 0), typically used for signaling or identification.

```go
type Empty struct{}

func main() {
    var e Empty
    fmt.Println(unsafe.Sizeof(e)) // prints 0
}
```

### 3. Methods on `struct`, object-oriented programming, and the relationship with `interface`

In Go, methods can be bound to a `struct`, which lets you mimic object-oriented programming (OOP). Methods are functions defined on a `struct` and can use either value receivers or pointer receivers.

```go
type Rectangle struct {
    Width, Height float64
}

// value receiver method
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// pointer receiver method
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

func main() {
    r := Rectangle{10, 20}
    fmt.Println(r.Area()) // prints 200

    r.Scale(2)
    fmt.Println(r.Area()) // prints 800
}
```

`interface` is the key to polymorphism in Go. A `struct` satisfies an interface by implementing the methods defined in that interface.

```go
type Shape interface {
    Area() float64
}

type Circle struct {
    Radius float64
}

func (c Circle) Area() float64 {
    return 3.14 * c.Radius * c.Radius
}

func main() {
    var s Shape
    s = Circle{10}
    fmt.Println(s.Area()) // prints 314
}
```

### 4. Composition and aggregation

#### Composition

Composition represents a strong ownership relationship, where the child object's lifecycle depends on the parent's. If the parent is destroyed, so are the children. In Go, composition is typically achieved by nesting one struct inside another.

```go
package main

import "fmt"

// define a Base struct
type Base struct {
    Name string
}

// define a method for Base
func (b Base) SayHello() {
    fmt.Println("Hello, my name is", b.Name)
}

// define a struct that contains Base
type Derived struct {
    Base
    Age int
}

func main() {
    d := Derived{
        Base: Base{Name: "Alice"},
        Age:  30,
    }

    // call Base's method directly
    d.SayHello() // prints "Hello, my name is Alice"
}
```

#### Aggregation

Aggregation represents a weak ownership relationship, where the child object's lifecycle is independent of the parent's. A child can be shared among multiple parents. In Go, aggregation is typically done via pointers — the parent holds a pointer to the child.

```go
package main

import "fmt"

// define the Engine struct
type Engine struct {
    Power int
}

// define the Car struct, aggregation via pointer
type Car struct {
    Brand  string
    Engine *Engine // aggregation, holds a pointer
}

func main() {
    e := &Engine{Power: 200}
    c1 := Car{Brand: "Toyota", Engine: e}
    c2 := Car{Brand: "Honda", Engine: e}

    fmt.Println(c1.Brand, "with power", c1.Engine.Power) // prints "Toyota with power 200"
    fmt.Println(c2.Brand, "with power", c2.Engine.Power) // prints "Honda with power 200"
}
```

### 5. Zero-value initialization

In Go, every variable is automatically initialized to its zero value upon declaration. For a `struct`, each field is initialized to the zero value of its type.

```go
type Person struct {
    Name  string
    Age   int
    Email string
}

func main() {
    var p Person
    fmt.Println(p) // prints { 0 }
}
```

### 6. Deep copy and shallow copy

In Go, assignment creates a shallow copy of a `struct`. When you need a deep copy, reference-type fields have to be copied manually.

#### Shallow copy

A shallow copy is made by directly assigning the struct or its pointer, which copies the struct's fields but not the underlying data pointed to by reference-type fields. Changing some fields of a shallow-copied struct won't affect the original, unless those fields are reference types (pointers, slices, maps, etc.) — in that case, both share the same underlying data.

```go
package main

import "fmt"

type Person struct {
    Name   string
    Age    int
    Friends []string
}

func main() {
    p1 := Person{Name: "Alice", Age: 30, Friends: []string{"Bob", "Charlie"}}
    p2 := p1 // shallow copy

    p2.Name = "Bob"
    p2.Friends[0] = "David"

    fmt.Println(p1.Name)   // prints "Alice"
    fmt.Println(p1.Friends) // prints "[David Charlie]"
    fmt.Println(p2.Name)   // prints "Bob"
    fmt.Println(p2.Friends) // prints "[David Charlie]"
}
```

In this example, `p1` and `p2` are two independent struct instances. Changing `p2.Name` doesn't affect `p1.Name`. But since `Friends` is a slice (a reference type), `p1.Friends` and `p2.Friends` share the same underlying data, so changing `p2.Friends` also changes `p1.Friends`.

#### Deep copy

A deep copy duplicates the entire struct along with all nested reference-type fields, producing a fully independent copy where changes to the new struct don't affect the original. Deep copies usually need to be implemented manually, especially for structs containing reference types.

```go
package main

import "fmt"

// define the Person struct
type Person struct {
    Name    string
    Age     int
    Friends []string
}

// deep copy function
func (p Person) DeepCopy() Person {
    // copy the basic fields
    newPerson := p

    // manually copy reference-type fields
    newPerson.Friends = make([]string, len(p.Friends))
    copy(newPerson.Friends, p.Friends)

    return newPerson
}

func main() {
    p1 := Person{Name: "Alice", Age: 30, Friends: []string{"Bob", "Charlie"}}
    p2 := p1.DeepCopy() // deep copy

    p2.Name = "Bob"
    p2.Friends[0] = "David"

    fmt.Println(p1.Name)    // prints "Alice"
    fmt.Println(p1.Friends) // prints "[Bob Charlie]"
    fmt.Println(p2.Name)    // prints "Bob"
    fmt.Println(p2.Friends) // prints "[David Charlie]"
}
```

In this example, implementing a `DeepCopy` method ensures `p2` is a fully independent copy of `p1` — changes to `p2` don't affect `p1`, including reference-type fields.

#### Summary

- **Shallow copy**: achieved by direct assignment; copies value-type fields, but reference-type fields share the same underlying data.
- **Deep copy**: requires manual implementation; copies both value-type and reference-type fields, producing a fully independent copy.

When a struct has reference-type fields like slices, maps, or pointers, the two structs produced by assignment share the underlying data — change one side and the other follows. To isolate them, you have to deep copy manually.

### 7. Method sets

Method sets determine whether a type implements a given interface. For type T, its method set includes all methods declared with value receivers. For type *T, its method set includes all methods declared with both value receivers and pointer receivers.

```go
type Person struct {
    Name string
}

func (p Person) SayHello() {
    fmt.Println("Hello, my name is", p.Name)
}

func (p *Person) SetName(name string) {
    p.Name = name
}

func main() {
    p := Person{Name: "Alice"}
    p.SayHello() // prints "Hello, my name is Alice"

    p.SetName("Bob")
    p.SayHello() // prints "Hello, my name is Bob"
}
```

In Go, method set inheritance follows the struct composition rules. Struct composition works by nesting other structs, which lets a struct "inherit" methods from multiple base structs. However, if nested structs have methods with the same name, you need to explicitly specify which base's method to access — otherwise it's a compile error.

#### Method set inheritance rules

When a struct nests another struct, it "inherits" the nested struct's methods. This means you can call the nested struct's methods directly without explicitly accessing the nested struct.

##### Example: single inheritance

```go
package main

import "fmt"

type Base struct{}

func (b Base) SayHello() {
    fmt.Println("Hello from Base")
}

type Derived struct {
    Base
}

func main() {
    d := Derived{}
    d.SayHello() // prints "Hello from Base"
}
```

In this example, the `Derived` struct nests the `Base` struct, so it can directly call `Base`'s `SayHello` method.

##### Example: multiple inheritance (method conflict)

When a struct nests multiple structs and those nested structs have methods with the same name, you need to explicitly specify which base's method to call.

```go
package main

import "fmt"

type A struct{}

func (a A) SayHello() {
    fmt.Println("Hello from A")
}

type B struct{}

func (b B) SayHello() {
    fmt.Println("Hello from B")
}

type C struct {
    A
    B
}

func main() {
    c := C{}
    // c.SayHello() // compile error: ambiguous selector c.SayHello
    c.A.SayHello() // prints "Hello from A"
    c.B.SayHello() // prints "Hello from B"
}
```

In this example, the `C` struct nests both `A` and `B`, and both have a `SayHello` method. Calling `c.SayHello()` directly causes a compile error because the compiler can't determine which `SayHello` to call. You have to explicitly specify `c.A.SayHello()` or `c.B.SayHello()`.

##### Summary

Methods on nested structs are promoted to the outer level — you don't need the full path to call them. When two nested structs have the same method name, `c.SayHello()` won't compile; you must write `c.A.SayHello()` or `c.B.SayHello()`.

### 8. Struct tags

Struct tags add metadata to fields, typically used with reflection, especially during serialization and deserialization (e.g., JSON, XML).

```go
type Person struct {
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email,omitempty"` // ignored if the field value is empty
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    data, _ := json.Marshal(p)
    fmt.Println(string(data)) // prints {"name":"Alice","age":30}
}
```

### 9. Reflection and `struct`

Reflection reads types and values at runtime: `reflect.TypeOf` gets the type, `NumField` and `Field` walk through each field, and the tags on each field come along too.

```go
import (
    "fmt"
    "reflect"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    t := reflect.TypeOf(p)
    for i := 0; i < t.NumField(); i++ {
        field := t.Field(i)
        fmt.Println(field.Name, field.Tag)
    }
}
```

### 10. Visibility rules

In Go, field and method visibility is determined by the first letter of the name. If the name starts with an uppercase letter, the field or method is exported (public); if it starts with lowercase, it's unexported (private).

```go
type Person struct {
    Name  string // public
    email string // private
}

func main() {
    p := Person{Name: "Alice", email: "alice@example.com"}
    fmt.Println(p.Name) // prints "Alice"
    // fmt.Println(p.email) // compile error, the email field is private
}
```

### 11. JSON serialization and deserialization

The `encoding/json` package makes it easy to serialize a `struct` to JSON or deserialize JSON back to a `struct`.

```go
import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    data, _ := json.Marshal(p)
    fmt.Println(string(data)) // prints {"name":"Alice","age":30}

    var p2 Person
    json.Unmarshal(data, &p2)
    fmt.Println(p2) // prints {Alice 30}
}
```

### 12. Types

Promotion and same-named fields

Fields of nested structs are promoted to the outer level: when the outer struct has no member with the same name, accessing `b.Name` directly is equivalent to accessing `b.A.Name`.

```go
package main

import "fmt"

type A struct {
    Name string
}

type B struct {
    A
    Age int
}

func main() {
    b := B{}
    b.Name = "Alice" // equivalent to b.A.Name = "Alice"; Name is promoted from A to B
    fmt.Println(b.Name) // prints "Alice"
}
```

When two nested structs share the same member name, promotion stops: for example, if `D` embeds both `B` and `C`, and both have `A.Name`, then `d.Name` fails to compile with `ambiguous selector` — you must write the full `d.B.Name` or `d.C.Name` (section 13 covers exactly this case).

### 13. Nesting and diamond inheritance

When multiple nested structs contain same-named fields, directly accessing those fields is ambiguous. The fix is to explicitly specify the nested struct.

```go
type A struct {
    Name string
}

type B struct {
    A
    Age int
}

type C struct {
    A
    Email string
}

type D struct {
    B
    C
}

func main() {
    d := D{}
    d.B.Name = "Alice"
    d.C.Name = "Bob"

    fmt.Println(d.B.Name) // prints "Alice"
    fmt.Println(d.C.Name) // prints "Bob"
}
```

### Summary

The bottom line here: field types and alignment determine memory usage, an empty `struct{}` is 0 bytes; value receivers and pointer receivers determine the method set, which in turn determines whether a type can satisfy an interface; use embedding for composition, pointers for aggregation; and serialization relies on field names in tags.

## References

- [Language Spec · Types](https://go.dev/ref/spec#Types)
- [Language Spec · Struct types](https://go.dev/ref/spec#Struct_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [String](/type/String.md)
- [Switch](/type/Switch.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [String](/type/String.md)
