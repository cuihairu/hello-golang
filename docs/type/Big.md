In some scenarios, numeric computation cannot tolerate the precision loss of `float64`; for those, you can use the `math/big` package to do high-precision arithmetic.

### Choosing a High-Precision Numeric Type

The `math/big` package in the Go standard library provides high-precision integer, floating-point, and rational types, and can handle arbitrary-precision numeric computation.

- **`big.Int`**: for high-precision integer arithmetic.
- **`big.Float`**: for high-precision floating-point arithmetic.
- **`big.Rat`**: for high-precision rational arithmetic.

#### Example: Using `big.Float`

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// create two high-precision floating-point numbers
	a := new(big.Float).SetFloat64(1.0 / 3.0)
	b := new(big.Float).SetFloat64(1.0 / 3.0)

	// perform the addition
	c := new(big.Float).Add(a, b)

	// print the result
	fmt.Printf("a: %.50f\n", a)
	fmt.Printf("b: %.50f\n", b)
	fmt.Printf("c: %.50f\n", c)
}
```

In this example, `big.Float` is used for high-precision floating-point computation, avoiding the precision loss problem in floating-point arithmetic.

### Use Cases for High-Precision Types

- **Financial computing**: in financial applications, money calculations demand very high precision and cannot accept the errors introduced by floating-point arithmetic.
- **Scientific computing**: in scientific and engineering computation, some applications need high-precision numeric results.
- **Cryptographic algorithms**: encryption and decryption operations sometimes require high-precision integer arithmetic.

### Notes

- **Performance**: high-precision numeric types are usually slower than native floating-point types, because they need more memory and computation.
- **Complexity**: using high-precision numeric types can make the code more complicated, requiring more code to handle their initialization and arithmetic.

### Summary

What `math/big` buys you is precision, at the cost of being slower and more verbose than native types (see the notes above). Use it where precision cannot go wrong (finance, scientific computing); for everyday display and statistics, `float64` is enough.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [math/big standard library](https://pkg.go.dev/math/big)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [BaseConv](/type/BaseConv.md)
- [Bool](/type/Bool.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BaseConv](/type/BaseConv.md)
- [Bool](/type/Bool.md)
