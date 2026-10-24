### Polymorphism of Interfaces

In Go, polymorphism is achieved through interfaces: the concrete type of a value can differ, and as long as the methods match, the same piece of code can operate on it without caring about its concrete type.

### 1. An Example of Polymorphism

The following example shows how to implement polymorphism with interfaces:

```go
package main

import "fmt"

// define an interface
type Speaker interface {
    Speak() string
}

// different types that implement the interface
type Person struct {
    Name string
}

func (p Person) Speak() string {
    return "Hi, I'm " + p.Name
}

type Dog struct {
    Name string
}

func (d Dog) Speak() string {
    return "Woof, I'm " + d.Name
}

// a function that takes an interface-typed parameter
func greet(s Speaker) {
    fmt.Println(s.Speak())
}

func main() {
    p := Person{Name: "Alice"}
    d := Dog{Name: "Rover"}

    greet(p) // prints: Hi, I'm Alice
    greet(d) // prints: Woof, I'm Rover
}
```

In this example, both `Person` and `Dog` implement `Speaker`. `greet` only knows the interface; it doesn't care what the concrete type is.

### 2. How Polymorphism Is Implemented Under the Hood

In Go, interface polymorphism is implemented through the following mechanisms:

1. **Interface type and method table**:
   - Every interface type has a method table, which is an array of function pointers recording the implementation addresses of the interface's methods.
   - When an interface variable is assigned a concrete type, the interface's internal structure includes a pointer to a type descriptor and a pointer to the actual value.

2. **The interface's internal structure**:
   - **Interface struct**: the underlying struct of an interface usually contains two fields: the type descriptor and the pointer to the actual value.
   - **Type descriptor**: describes the concrete implementation of the interface type, including the method table and the type information.

**Example: The interface's internal structure**

```go
// simplified sketch (`type` is a Go keyword and cannot be used as a field name, so `typ` is used here;
// the real implementation is the eface, iface, and itab in the runtime package)
type _interface struct {
    typ   *typeDescriptor // pointer to the type descriptor
    value unsafe.Pointer  // pointer to the actual value
}

type typeDescriptor struct {
    methodTable *methodTable // method table
    typeName    string       // type name
}
```

3. **The method call process**:
   - When an interface method is called, the Go runtime uses the interface's type descriptor to find the corresponding method table.
   - It finds the matching method implementation from the method table and calls it.

**Example: Method table**

```go
type methodTable struct {
    methods []func()
}
```

### 3. Source of the Interface Implementation (Simplified)

The underlying implementation of interfaces in Go's standard library is relatively complex. The following simplified example shows how interfaces use the method table and type descriptor to implement polymorphism.

**Simplified code example**

```go
package main

import (
    "fmt"
)

// interface definition
type Speaker interface {
    Speak() string
}

// a type that implements the interface
type Person struct {
    Name string
}

func (p Person) Speak() string {
    return "Hi, I'm " + p.Name
}

type Dog struct {
    Name string
}

func (d Dog) Speak() string {
    return "Woof, I'm " + d.Name
}

func greet(s Speaker) {
    fmt.Println(s.Speak())
}

func main() {
    p := Person{Name: "Alice"}
    d := Dog{Name: "Rover"}

    greet(p)
    greet(d)
}
```

**Underlying implementation (simplified assembly example)**

```assembly
TEXT runtime.callMethod(SB), NOSPLIT, $0
    MOVQ    8(SP), SI          // get the interface's type descriptor
    MOVQ    16(SP), CX         // get the expected type descriptor
    MOVQ    24(SP), DI         // get the interface's value
    CMPQ    SI, CX             // compare the type descriptors
    JNE     notMatch           // if they don't match, jump to error handling
    MOVQ    DI, 32(SP)         // move the value part to the return value
    RET
notMatch:
    // handle the type mismatch case
    RET
```

### 4. Comparing Interface Polymorphism with Other Languages

Compared with other programming languages (such as C++, Java, and Python), Go's interfaces have the following characteristics:

- **Go's interfaces**: the set of methods defines the interface's behavior, and there is no need to explicitly declare the implementation relationship. As long as a type implements the methods the interface requires, it implements that interface.
- **C++ polymorphism**: polymorphism is implemented through virtual functions; you must explicitly declare the interface (an abstract class) and use virtual functions.
- **Java interfaces**: interfaces are defined explicitly, and the implementation relationship must be declared when implementing the interface.
- **Python's dynamic typing**: interfaces (duck typing) are implicit; a type's behavior depends on whether it implements certain methods.

### Summary

- **Interface polymorphism**: lets objects of different types interact through the same interface methods, producing different behaviors.
- **Underlying implementation**: implemented through the type descriptor and method table. The interface contains a type descriptor and a pointer to the actual value.
- **Call flow**: get the type descriptor, look up the method table, and call the matching method implementation.
- **Comparison**: Go does not require explicitly declaring the implementation relationship, C++ requires an abstract class and virtual functions, Java requires declaring the implementation relationship, and Python relies on duck typing.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)


## Sibling pages

- [Embedding](/oop/Embedding.md)
- [Interface](/oop/Interface.md)
- [PointerReceiver](/oop/PointerReceiver.md)
- [TypeAssertion](/oop/TypeAssertion.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Embedding](/oop/Embedding.md)
