### Type Assertion

In Go, a type assertion is a mechanism for checking and converting an interface type. It lets you convert an interface type to a concrete type and check whether the interface's dynamic type matches a particular type.

### 1. Basic Syntax of Type Assertion

The syntax for a type assertion is as follows:

```go
value, ok := x.(T)
```

Where:
- `x` is an interface variable.
- `T` is the concrete type you want to assert to.
- `value` is the value of the concrete type when the assertion succeeds.
- `ok` is a boolean indicating whether the assertion succeeded.

**Example: Type assertion**

```go
package main

import (
    "fmt"
)

func main() {
    var i interface{} = "hello"

    // type assertion
    s, ok := i.(string)
    if ok {
        fmt.Println("String value:", s)
    } else {
        fmt.Println("Not a string")
    }
}
```

### 2. Use Cases for Type Assertion

- **Type checking**: check whether an interface's dynamic type matches a particular concrete type.
- **Type conversion**: convert an interface type to a concrete type in order to call that type's methods.

### 3. How Type Assertion Is Implemented Under the Hood

In Go, the underlying implementation of a type assertion involves the interface's type descriptor and method table. The concrete implementation works as follows:

1. **Interface structure**: an interface variable contains two parts in memory:
   - `typ`: a pointer to the type descriptor (`type` is a Go keyword and cannot be used as a field name).
   - `value`: a pointer to the actual value.

2. **Type descriptor**: the type descriptor contains the type information and the method table. The method table is an array of function pointers, where each pointer points to the actual function implementing an interface method.

3. **The assertion process**:
   - **Check the type**: use the interface's type descriptor to check whether `x`'s actual type matches `T`.
   - **Convert the type**: if it matches, convert the interface's value part to type `T`.

**Example: A simplified version of the underlying implementation** (the real implementation is the `eface`, `iface`, and `itab` in the `runtime` package)

```go
type _interface struct {
    typ   *typeDescriptor // type descriptor
    value unsafe.Pointer  // the actual value
}

type typeDescriptor struct {
    methodTable *methodTable // method table
    typeName    string       // type name
}

type methodTable struct {
    methods []func()
}
```

### 4. An Assembly Code Example

Go's assembly code shows the underlying implementation of a type assertion. The following is a simplified assembly example showing how a type assertion is performed (for the `amd64` architecture):

```assembly
TEXT runtime.typeAssert(SB), NOSPLIT, $0
	MOVQ	8(SP), SI          // get the interface's type descriptor
	MOVQ	16(SP), CX         // get the expected type descriptor
	MOVQ	24(SP), DI         // get the interface's value
	CMPQ	SI, CX             // compare the type descriptors
	JNE		notMatch          // if they don't match, jump to error handling
	MOVQ	DI, 32(SP)         // move the value part to the return value
	RET
notMatch:
	// handle the type mismatch case
	RET
```

### 5. Advanced Uses of Type Assertion

**The bare value of a type assertion** (the non-`ok` form):

```go
s := i.(string)  // assert directly; panics if it fails
```

**Error handling for a type assertion**:

```go
s, ok := i.(string)
if !ok {
    // handle the failed assertion case
}
```

### 6. Performance of Type Assertion

Type assertions are cheap. The cost comes mostly from two places:
- **Type checking**: the interface's type descriptor must be checked for a match.
- **Memory access**: the interface's value and type descriptor must be read.

Avoid assertions on performance-sensitive code paths to skip these checks and conversions.

### Summary

- **Type assertion**: lets you convert an interface type to a concrete type and check the interface's dynamic type.
- **Underlying implementation**: involves the interface's type descriptor and method table, and asserts by checking the type descriptor.
- **Assembly code**: shows the underlying operations of a type assertion, including the type check and conversion.
- **Performance**: the performance overhead of a type assertion is small, but it should be used carefully in performance-sensitive code.

A bare `i.(T)` panics on failure, while `value, ok := i.(T)` does not; use the latter when you are unsure what type the interface holds.

## References

- [Official FAQ · Type system](https://go.dev/doc/faq)
- [Language spec · Interface types](https://go.dev/ref/spec#Interface_types)
- [Effective Go · Methods](https://go.dev/doc/effective_go#methods)
- [Effective Go · Embedding](https://go.dev/doc/effective_go#embedding)
- [Language spec · Type assertions](https://go.dev/ref/spec#Type_assertions)
- [Effective Go · interface conversions](https://go.dev/doc/effective_go#interface_conversions)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Poly](/oop/Poly.md)
