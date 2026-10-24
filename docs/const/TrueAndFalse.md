In Go, `true` and `false` are predefined constants of the boolean type, used to represent logical truth and logical falsity.

### The boolean type

The boolean type has only two predefined values: `true` and `false`. In Go, the boolean type is used for conditionals, logical operations, and control flow.

#### Declaration and initialization

```go
var b1 bool = true
var b2 = false // the type is inferred as bool
```

#### Logical operations

Boolean values can take part in logical operations, including logical AND (`&&`), logical OR (`||`), and logical NOT (`!`).

```go
fmt.Println(true && false) // prints: false
fmt.Println(true || false) // prints: true
fmt.Println(!true)         // prints: false
```

#### Conditional evaluation

Boolean values are commonly used in the condition part of `if`, `for`, `switch`, and similar statements.

```go
if true {
    fmt.Println("This condition is true")
}

for i := 0; i < 3; i++ {
    fmt.Println(i)
}

switch true {
case true:
    fmt.Println("This case is true")
default:
    fmt.Println("This case is false")
}
```

### Where to use it

- **Conditionals**: the condition position of `if`, `for`, and `switch`.
- **Logical operations**: `&&`, `||`, and `!` combine several conditions into one.
- **Function return values**: return a boolean to say whether a condition is satisfied, and the caller can branch on it directly.

### Example code

```go
package main

import "fmt"

func main() {
    var isOpen bool = true
    var isFound = false // the type is inferred as bool

    if isOpen {
        fmt.Println("The door is open")
    }

    if !isFound {
        fmt.Println("Item not found")
    }

    fmt.Println(true && false) // prints: false
    fmt.Println(true || false) // prints: true
}
```

### Summary

`true` and `false` are the predefined constants of the boolean type; `&&`, `||`, and `!` all operate on top of them, and the conditions of `if`, `for`, and `switch` use boolean values too.

## References

- [Language specification · Constant declarations](https://go.dev/ref/spec#Constant_declarations)
- [Official blog · Constants](https://go.dev/blog/constants)
- [Language specification · Predeclared identifiers](https://go.dev/ref/spec#Predeclared_identifiers)

## Sibling pages

- [Cant](/const/Cant.md)
- [Iota](/const/Iota.md)
- [Nil](/const/Nil.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Cant](/const/Cant.md)
