In Go, a type assertion converts an interface-typed variable into a concrete type, pulling the underlying concrete value out of the interface value.

### Type assertion syntax

The basic syntax for a type assertion is:

```go
value, ok := interfaceVariable.(ConcreteType)
```

- `interfaceVariable` is the interface-typed variable.
- `ConcreteType` is the concrete type you want to convert to.
- `value` is the concrete value after the conversion.
- `ok` is a boolean indicating whether the type assertion succeeded.

If the type assertion succeeds, `ok` is `true` and `value` holds the concrete value; otherwise `ok` is `false` and `value` holds the zero value of that type.

### Examples

Here are some examples of using type assertions:

#### Successful type assertion

```go
package main

import (
    "fmt"
)

func main() {
    var i interface{} = "hello"

    // successful type assertion
    s, ok := i.(string)
    if ok {
        fmt.Println("String value:", s) // prints: String value: hello
    } else {
        fmt.Println("type assertion failed")
    }
}
```

#### Failed type assertion

```go
package main

import (
    "fmt"
)

func main() {
    var i interface{} = 42

    // failed type assertion
    s, ok := i.(string)
    if ok {
        fmt.Println("String value:", s)
    } else {
        fmt.Println("type assertion failed") // prints: type assertion failed
    }
}
```

#### Type assertion without the `ok` variable

If you're sure the type assertion will succeed, you can omit the `ok` variable. If the assertion fails, the program panics:

```go
package main

import (
    "fmt"
)

func main() {
    var i interface{} = "hello"

    // type assertion without the ok variable (the assertion is known to succeed)
    s := i.(string)
    fmt.Println("String value:", s) // prints: String value: hello

    // type assertion without the ok variable (panics on failure)
    // n := i.(int) // panics at runtime
}
```

### Use cases for type assertions

1. **Extracting a concrete value from an interface**: when handling an interface-typed variable, a type assertion gets you the concrete value.
2. **Type-safe conversion**: checking `ok` tells you whether the assertion succeeded, which avoids runtime errors.
3. **Together with a type switch**: `switch v := x.(type)` lets you list several types at once and handle each one.

### Example: handling interface values of multiple types

```go
package main

import (
    "fmt"
)

func main() {
    var i interface{} = "hello"

    switch v := i.(type) {
    case string:
        fmt.Println("String value:", v)
    case int:
        fmt.Println("Integer value:", v)
    default:
        fmt.Println("Unknown type")
    }
}
```

In this example, combining a type assertion with a type switch lets you handle different concrete types of an interface value separately.

### Summary

A type assertion pulls the concrete value out of an interface value. The form with `ok` returns the zero value and `false` on failure, the form without `ok` panics straight away, and a type switch branches on multiple types in one place.

## References

- [Language Spec · Types](https://go.dev/ref/spec#Types)
- [Language Spec · Type assertions](https://go.dev/ref/spec#Type_assertions)

## Sibling pages

- [Array](/type/Array.md)

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
