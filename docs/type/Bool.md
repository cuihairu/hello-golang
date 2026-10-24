In Go, the `bool` type is a basic data type used to represent boolean values, that is, `true` and `false`. It is commonly used in conditionals and logical operations. In Go, a `bool` variable can be assigned with the keywords `true` and `false`.

### Declaration and Initialization

You can declare and initialize a `bool` variable like this:

```go
package main

import "fmt"

func main() {
    var a bool       // declared but not initialized, defaults to false
    var b bool = true  // declared and initialized to true
    c := false        // short declaration, initialized to false
    fmt.Println(a, b, c) // false true false
}
```

### Use Cases

The `bool` type is typically used in conditionals, such as `if` statements and loop control:

```go
a := false
b := true

if a {
    fmt.Println("a is true")
} else {
    fmt.Println("a is false")
}

for b {
    fmt.Println("This will print once because b is true")
    b = false
}
```

### Logical Operations

Go provides the basic logical operators to work with the `bool` type:

- `&&`: logical AND operator
- `||`: logical OR operator
- `!`: logical NOT operator

Example:

```go
x := true
y := false

fmt.Println(x && y)  // prints false
fmt.Println(x || y)  // prints true
fmt.Println(!x)      // prints false
```

### Notes

1. **Type conversion**: Go does not allow implicit conversion between other types and `bool`. For example, you cannot directly convert the integer `0` or `1` to `false` or `true`.
2. **Default value**: the default value of the `bool` type is `false`. If a boolean variable is not explicitly initialized, its value will be `false`.

### Example Code

Declaration, initialization, and logical operations all in one run:

```go
package main

import "fmt"

func main() {
    var flag bool
    fmt.Println("flag:", flag) // prints flag: false

    flag = true
    if flag {
        fmt.Println("flag is true")
    }

    var isReady bool = false
    if !isReady {
        fmt.Println("isReady is false")
    }

    x, y := true, false
    fmt.Println("x && y:", x && y) // prints x && y: false
    fmt.Println("x || y:", x || y) // prints x || y: true
    fmt.Println("!x:", !x)         // prints !x: false
}
```

To sum up the usage above: `bool` has only two values, an uninitialized declaration is `false`, it cannot be converted with integers, and in a conditional you can just write the variable name directly — no need for `flag == true`.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Boolean Types](https://go.dev/ref/spec#Boolean_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Big](/type/Big.md)
- [Byte](/type/Byte.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Big](/type/Big.md)
- [Byte](/type/Byte.md)
