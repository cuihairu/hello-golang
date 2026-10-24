A constant is a value fixed at compile time that can't change while the program runs; a literal is a concrete value written directly in the code. Here is how to write each:

### Constants

A constant is a value that stays fixed throughout the program and cannot be modified once defined. In Go, a constant can be a basic type such as a number, a boolean, or a string, and its value is already settled at compile time.

#### Defining a constant

To define a constant in Go, use the `const` keyword. The syntax is:

```go
const identifier [type] = value
```

- `identifier` is the name of the constant.
- `[type]` is an optional type specifier; it can be omitted, in which case the type is inferred automatically from the assigned value.
- `value` is the value of the constant; it must be determinable at compile time.

For example:
```go
const pi = 3.14159
const maxRetry = 3
const welcomeMessage = "Hello, World!"
```

#### Constant enumerations

Constant enumerations are a common idiom that cuts down on repeated definitions:

```go
const (
    Monday    = 1
    Tuesday   = 2
    Wednesday = 3
    Thursday  = 4
    Friday    = 5
)
```

#### Constant expressions

A constant can be produced by basic arithmetic done at declaration time, for example:

```go
const (
    a = 10
    b = 20
    c = a + b // a constant expression
)
```

### Literals

Literals are symbols that stand for fixed values; a literal can be the concrete value of a constant, a variable, or an expression. Go has several kinds of literals:

- **Integer literals**: `42`, `-100`, `0xFF` (hexadecimal), `077` (octal), and so on.
- **Floating-point literals**: `3.14`, `1.5e-10`, and so on.
- **Complex literals**: `3.14i`, `1 + 2i`, and so on.
- **String literals**: `"Hello, World!"`, `` `multi-line
  string` ``, and so on.
- **Boolean literals**: `true` and `false`.
- **Rune literals**: `'a'`, `'\n'`, `'\u2318'`, and so on.

#### Example

```go
package main

import "fmt"

func main() {
    const pi = 3.14159
    fmt.Println("Pi value is", pi)

    const (
        Monday = 1
        Tuesday = 2
        Wednesday = 3
        Thursday = 4
        Friday = 5
    )
    fmt.Println("Monday is", Monday)
}
```

### Summary

- **Constants** are declared with `const` and cannot be modified at runtime. Any value in the program that never changes belongs here, so a reader can tell at a glance that it won't move.
- **Literals** are values written directly in the code, like `42`, `3.14`, `"Hello, World!"` — no declaration needed.
- A constant's value must be computable at compile time. If the compiler can't evaluate it, it errors out right there; the mistake never waits until runtime to blow up.

## References

- [Language specification · Constant declarations](https://go.dev/ref/spec#Constant_declarations)
- [Official blog · Constants](https://go.dev/blog/constants)

## Sibling pages

- [Cant](/const/Cant.md)
- [Iota](/const/Iota.md)
- [Nil](/const/Nil.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Cant](/const/Cant.md)
