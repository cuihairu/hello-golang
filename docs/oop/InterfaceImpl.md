At the bottom, an interface value is just a pair: a pointer to a type descriptor, plus a pointer to the actual data. This page follows the data structure, the method table, and the assembly call, and finishes with the `nil` interface and the empty interface.

### 1. The Underlying Data Structure of an Interface

An interface in Go has two main parts:

1. **Type information (Type Descriptor)**: describes the concrete type that implements the interface, including its method table and type info.
2. **Value information (Value)**: stores the actual value that implements the interface, i.e. the object instance.

The underlying structure of an interface can be simplified to the following (the real implementation is the `eface`, `iface`, and `itab` structs in the `runtime` package; note that `type` is a Go keyword and cannot be used as a field name, so `typ` is used here):

```go
type _interface struct {
    typ   *typeDescriptor // type descriptor
    value unsafe.Pointer  // points to the actual value
}
```

### 2. The Type Descriptor

`typeDescriptor` is an internal struct that holds a type's metadata, such as its method table and type name. Every type that implements an interface has a corresponding type descriptor. The method table is an array of function pointers, where each pointer points to the actual function that implements an interface method.

**Example: An interface's type descriptor**

```go
type typeDescriptor struct {
    methodTable *methodTable // method table
    typeName    string       // type name
    // other metadata
}

type methodTable struct {
    // array of function pointers
    methodPtrs []uintptr
}
```

### 3. The Method Table

The method table is an array of function pointers, where each pointer points to an implementation of an interface method. The method table is what lets Go dispatch interface method calls dynamically at runtime.

**Example: Method table structure**

```go
type methodTable struct {
    methods []func()
}
```

### 4. Source of the Interface Implementation (Simplified)

The underlying implementation of interfaces in Go's standard library is relatively complex. The following simplified example shows how interfaces use the method table and the type descriptor.

```go
package main

import (
    "fmt"
    "reflect"
)

// interface definition
type Speaker interface {
    Speak() string
}

// the type implements the interface
type Person struct {
    Name string
}

// implement the interface method
func (p Person) Speak() string {
    return "Hi, I'm " + p.Name
}

func main() {
    var s Speaker = Person{Name: "Alice"}

    // type assertion
    if person, ok := s.(Person); ok {
        fmt.Println("Person:", person.Name) // prints: Person: Alice
    } else {
        fmt.Println("Not a Person")
    }

    // use the reflect package to get the interface's underlying info
    t := reflect.TypeOf(s)
    fmt.Println("Type:", t) // prints: Type: main.Person
    fmt.Println("Value:", reflect.ValueOf(s)) // prints: Value: {Alice}
}
```

### 5. Low-level Implementation Example (Assembly)

Dynamic dispatch of interface methods ultimately comes down to a small piece of assembly. The following is a simplified example (for `amd64`):

**Example: Go assembly**

```assembly
TEXT runtime.reflectcall(SB), NOSPLIT, $0
	MOVQ	8(SP), SI
	MOVQ	16(SP), CX
	MOVQ	24(SP), DI
	CALL	runtime.callReflection
	RET
```

In the assembly above, the `reflectcall` function is what calls the interface's actual method. It loads the arguments into registers with `MOVQ` instructions and calls the `runtime.callReflection` function to execute the interface method.

### 6. The Interface Call Flow

When an interface method is called, Go's runtime finds the concrete implementation using the interface's type descriptor and method table. The flow is:

1. **Get the type descriptor**: pull the type descriptor out of the interface; it contains the method table and the type name.
2. **Get the method table**: pull the method table out of the type descriptor; it contains the addresses of the interface method implementations.
3. **Call the method**: call the concrete implementation function via the function pointer in the method table.

### 7. The Interface Zero Value and the Empty Interface

- **The interface zero value**: an interface's zero value is `nil`, meaning the interface variable has not been initialized. Calling a method on an uninitialized interface causes a runtime error.
- **The empty interface**: `interface{}` can hold data of any type, because it has no method set. The empty interface is very useful in generic functions and data structures.

**Example: The empty interface**

```go
package main

import "fmt"

func printAnything(i interface{}) {
    fmt.Println(i)
}

func main() {
    printAnything(42)         // integer
    printAnything("hello")    // string
    printAnything([]int{1, 2}) // slice
}
```

### Summary

- **Underlying data structure of an interface**: includes the type descriptor and the method table, used to store the interface's type info and method implementations.
- **Type descriptor**: contains the method table and the type name, used to describe the concrete type that implements the interface.
- **Method table**: an array of function pointers, used to store the implementations of interface methods.
- **Assembly example**: shows the interface's low-level operations and call flow.
- **Interface zero value and empty interface**: an interface's zero value is `nil`, and the empty interface can hold data of any type.

Once you understand "interface value = type pointer + data pointer", two questions are answered: why calling a method on a `nil` interface panics (the type pointer is empty, so there is no method table to look up); and why storing a pointer whose value is `nil` in an interface and then testing `== nil` gives `false` (the type pointer is not empty).

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
- [Language spec · Method sets](https://go.dev/ref/spec#Method_sets)


## Sibling pages

- [Embedding](/oop/Embedding.md)
- [Interface](/oop/Interface.md)
- [PointerReceiver](/oop/PointerReceiver.md)
- [Methods](/oop/Methods.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Methods](/oop/Methods.md)
