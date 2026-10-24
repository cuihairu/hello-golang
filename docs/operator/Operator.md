# Operators
Go's operators are broadly in line with the C family of languages; a few (such as increment/decrement, and the lack of a ternary operator) make their own trade-offs. Here they are listed by category, with example code.

### 1. Arithmetic operators

Arithmetic operators do addition `+`, subtraction `-`, multiplication `*`, division `/`, and remainder `%`; all of them are binary operations.

Example code:
```go
package main

import "fmt"

func main() {
    a := 10
    b := 3

    fmt.Println("a + b =", a + b)   // 13
    fmt.Println("a - b =", a - b)   // 7
    fmt.Println("a * b =", a * b)   // 30
    fmt.Println("a / b =", a / b)   // 3
    fmt.Println("a % b =", a % b)   // 1
}
```

### 2. Relational operators

Relational operators compare two values and produce a boolean result: `==`, `!=`, `>`, `<`, `>=`, `<=`.

Example code:
```go
package main

import "fmt"

func main() {
    a := 10
    b := 20

    fmt.Println("a == b =", a == b)   // false
    fmt.Println("a != b =", a != b)   // true
    fmt.Println("a > b =", a > b)     // false
    fmt.Println("a < b =", a < b)     // true
    fmt.Println("a >= b =", a >= b)   // false
    fmt.Println("a <= b =", a <= b)   // true
}
```

### 3. Logical operators

There are only three logical operators: AND `&&`, OR `||`, and NOT `!`; the operands are booleans.

Example code:
```go
package main

import "fmt"

func main() {
    a := true
    b := false

    fmt.Println("a && b =", a && b) // false
    fmt.Println("a || b =", a || b) // true
    fmt.Println("!a =", !a)         // false
}
```

### 4. Assignment operators

Besides plain `=` assignment, `+=`, `-=`, `*=`, `/=`, `%=` fold the operation and the assignment into a single step, equivalent to "compute first, then store".

Example code:
```go
package main

import "fmt"

func main() {
    a := 10
    a += 5
    fmt.Println("a += 5 =>", a) // 15

    a -= 3
    fmt.Println("a -= 3 =>", a) // 12

    a *= 2
    fmt.Println("a *= 2 =>", a) // 24

    a /= 4
    fmt.Println("a /= 4 =>", a) // 6

    a %= 5
    fmt.Println("a %= 5 =>", a) // 1
}
```

### 5. Bitwise operators

Bitwise operators work on the binary bits of an integer directly: bitwise AND `&`, bitwise OR `|`, bitwise XOR `^`, bitwise NOT `^`, left shift `<<`, right shift `>>`. Note that `^` has two identities: with two operands it is XOR, with one it is NOT.

Example code:
```go
package main

import "fmt"

func main() {
    a := 5    // 0101 in binary
    b := 3    // 0011 in binary

    fmt.Println("a & b =", a & b) // 0001 (1 in decimal)
    fmt.Println("a | b =", a | b) // 0111 (7 in decimal)
    fmt.Println("a ^ b =", a ^ b) // 0110 (6 in decimal)
    fmt.Println("^a =", ^a)       // 1010 (inverted bits of 5)
    fmt.Println("a << 1 =", a << 1) // 1010 (10 in decimal)
    fmt.Println("a >> 1 =", a >> 1) // 0010 (2 in decimal)
}
```

### 6. Conditional operators (Go has no ternary operator directly)

Go has no conditional operator of its own (like `? :`), but you can get the same effect with an `if` statement.

Example code:
```go
package main

import "fmt"

func main() {
    a := 10
    b := 20
    max := a

    if b > a {
        max = b
    }

    fmt.Println("Max =", max) // 20
}
```

### 7. Increment and decrement operators

Increment `++` and decrement `--` add one to or subtract one from a variable's value. They are statements, not expressions: there is no prefix form like `++a`, and you cannot nest them inside another expression.

Example code:
```go
package main

import "fmt"

func main() {
    a := 10
    a++
    fmt.Println("a++ =", a) // 11

    a--
    fmt.Println("a-- =", a) // 10
}
```

### Summary

Of the seven categories above, two places differ most from other languages: integer division `/` truncates the fraction outright (`10 / 3` gives `3`), and there is no ternary operator, so conditional values have to be written with `if`. Increment and decrement can only stand on their own as statements, which is also why they sit in the postfix position in `for i := 0; i < n; i++`.

## References

- [Language specification · Operators](https://go.dev/ref/spec#Operators)


## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [BitLen](/operator/BitLen.md)
- [Logical](/operator/Logical.md)
- [Receiver](/operator/Receiver.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Logical](/operator/Logical.md)
- [Receiver](/operator/Receiver.md)
