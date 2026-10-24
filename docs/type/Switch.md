### Type `switch` in Go


> Perspective: this page focuses on branching on the dynamic type of an interface; for the ordinary expression `switch` and its control-flow behavior, see the [switch statement notes](/syntax/Switch.md).
A type `switch` is a special form of Go's `switch` statement, used to branch on the dynamic type of an interface value. It is commonly used to handle interface variables of unknown type, letting the code perform different operations depending on the actual type.

### Syntax of a type `switch`

The syntax of a type `switch`:

```go
switch v := i.(type) {
case T1:
    // v is of type T1
case T2:
    // v is of type T2
default:
    // v is of some other type
}
```

- `i.(type)`: extracts the dynamic type of the interface `i`.
- `v`: in each `case`, `v` is the value of the concrete type of the interface `i`.
- `T1`, `T2`: concrete types.

### Example code

Dispatching on the type of the same interface value:

```go
package main

import (
    "fmt"
)

func doSomething(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("int value: %d\n", v)
    case string:
        fmt.Printf("string value: %s\n", v)
    case bool:
        fmt.Printf("bool value: %t\n", v)
    default:
        fmt.Printf("unknown type: %T\n", v)
    }
}

func main() {
    doSomething(10)
    doSomething("hello")
    doSomething(true)
    doSomething(3.14)
}
```

Output:

```
int value: 10
string value: hello
bool value: true
unknown type: float64
```

### How a type `switch` works

1. **Interface variable**: the operand of a type `switch` must be an interface variable, because only interface variables have a dynamic type.
2. **Type determination**: the `type` keyword in the `switch` statement obtains the dynamic type of the interface variable.
3. **Branch matching**: the matching `case` is selected based on the dynamic type; if no `case` matches, the `default` branch runs.
4. **Type assertion**: within each `case`, the interface variable can be asserted to the concrete type and assigned to the variable declared in the `switch` statement.

### Application scenarios for a type `switch`

A type `switch` is used when you hold an interface value and need to dispatch on its concrete type. Three common cases:

1. **Logging**: a log message may be a string, an `error`, or a struct — the handling differs, so a type `switch` routes each one separately.
2. **Generic programming**: when implementing generic data structures or algorithms, a type `switch` can be used to handle elements of different types.
3. **Interface implementation detection**: when implementing certain interfaces, a type `switch` can check the concrete type of an incoming parameter and handle it differently.

### Type `switch` versus an ordinary `switch`

- **Ordinary `switch`**: an ordinary `switch` statement branches on the value of a variable.
- **Type `switch`**: a type `switch` branches on the dynamic type of an interface variable.

Example comparison:

Ordinary `switch`:

```go
package main

import "fmt"

func main() {
    var x = 10
    switch x {
    case 1:
        fmt.Println("One")
    case 2:
        fmt.Println("Two")
    case 10:
        fmt.Println("Ten")
    default:
        fmt.Println("Unknown")
    }
}
```

Type `switch`:

```go
package main

import "fmt"

func main() {
    var i interface{} = 10
    switch v := i.(type) {
    case int:
        fmt.Println("int value:", v)
    case string:
        fmt.Println("string value:", v)
    default:
        fmt.Println("unknown type")
    }
}
```

### Summary

A type `switch` solves one thing: you have an interface value but don't know its dynamic type, so use `switch v := i.(type)` to dispatch on type, and `v` is the value of that type inside each `case`. The difference from an ordinary `switch` is only in the branching condition — one looks at the value, the other at the type.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Language spec · Type switches](https://go.dev/ref/spec#Type_switches)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/zh/glossary.md)
- [Struct](/type/Struct.md)
- [Template](/type/Template.md)
