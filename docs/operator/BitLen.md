Go has no `bit length` operator (some languages do). Bit length means the number of binary bits needed to represent the integer.

### Computing the bit length

Two ways to do it in Go: call `bits.Len`, or write a right-shift counter yourself.

#### 1. Using the `math/bits` package

`bits.Len` from the `math/bits` package gives you the bit length of an unsigned integer directly.

```go
package main

import (
    "fmt"
    "math/bits"
)

func main() {
    num := 23  // binary: 10111
    bitLength := bits.Len(uint(num))
    fmt.Println("Bit length of", num, "is:", bitLength) // prints: Bit length of 23 is: 5
}
```

In this example, the `bits.Len` function computes the bit length of an unsigned integer. For signed integers you first have to convert them to unsigned (for example using the `uint` type).

#### 2. Manual calculation

The hand-rolled way is to shift right repeatedly, incrementing a counter one step at a time:

```go
package main

import (
    "fmt"
)

func bitLength(n int) int {
    if n == 0 {
        return 1
    }
    length := 0
    for n > 0 {
        length++
        n >>= 1
    }
    return length
}

func main() {
    num := 23  // binary: 10111
    bitLength := bitLength(num)
    fmt.Println("Bit length of", num, "is:", bitLength) // prints: Bit length of 23 is: 5
}
```

Keep shifting the number right until it reaches 0; the counter's value is then the bit length. `n == 0` is handled separately and returns 1.

### Summary

- The Go language itself has no direct bit length operator.
- You can use the `bits.Len` function from the `math/bits` package to compute the bit length of an unsigned integer.
- You can also write the calculation by hand to get the bit length of an integer, which works with any integer type.

## References

- [Language specification · Operators](https://go.dev/ref/spec#Operators)

## Sibling pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [Bitwise](/operator/Bitwise.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Arithmetic](/operator/Arithmetic.md)
- [Assignment](/operator/Assignment.md)
- [Bitwise](/operator/Bitwise.md)
- [Cap](/operator/Cap.md)
- [Logical](/operator/Logical.md)
- [Operator](/operator/Operator.md)
- [Receiver](/operator/Receiver.md)
- [Relational](/operator/Relational.md)
- [TypeAssertion](/operator/TypeAssertion.md)
- [Unary](/operator/Unary.md)
