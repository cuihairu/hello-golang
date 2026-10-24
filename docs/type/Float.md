In Go, floating-point types are used to represent numbers with a decimal point. Go provides two floating-point types: `float32` and `float64`, corresponding to single-precision and double-precision floating-point numbers respectively. These types are used to handle decimal numbers that need a larger range or higher precision.

### Representation and Precision of Floating-Point Types

1. **float32**:
   - Occupies 32 bits (4 bytes) of memory.
   - Can represent about 6 decimal digits of precision.
   - Range is approximately `1.18e-38` to `3.4e38`.

2. **float64**:
   - Occupies 64 bits (8 bytes) of memory.
   - Can represent about 15-16 decimal digits of precision.
   - Range is approximately `2.23e-308` to `1.8e308`.

Go's floating-point numbers are represented and computed per the IEEE 754 standard; precision loss and rounding error are the inherent cost of this representation.

### Precision and Rounding Error

Although floating-point numbers can represent a wide range of values, some precision problems arise when doing floating-point arithmetic, mainly in the following areas:

- **Precision limits**: the precision of floating-point numbers is limited, and when computing over large ranges of values, precision loss can occur.

- **Rounding error**: because the internal representation of floating-point numbers has finite precision, some decimal numbers may not be representable exactly as binary floats, leading to rounding error.

- **Comparison uncertainty**: because of rounding error, equality comparisons (such as the `==` operator) can produce unexpected results. It is usually recommended to use approximate comparison methods for floating-point numbers to avoid these problems.

### Examples and Notes

```go
package main

import (
	"fmt"
)

func main() {
	var x float32 = 1.0 / 3.0
	var y float64 = 1.0 / 3.0

	fmt.Printf("float32: %.10f\n", x)
	fmt.Printf("float64: %.10f\n", y)
}
```

In the example above, even a simple division such as `1.0 / 3.0` is represented differently in `float32` and `float64`, which illustrates the effect of floating-point precision and rounding error.

### Summary

`float32` takes 4 bytes and about 6 decimal digits of precision; `float64` takes 8 bytes and about 15-16. To check whether two floating-point numbers are equal, do not use `==` directly — use approximate comparison instead; divisions like `1.0 / 3.0` yield a different number of decimal digits under the two types, and which one you pick depends on the precision you need.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Numeric Types](https://go.dev/ref/spec#Numeric_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Conv](/type/Conv.md)
- [HtmlTemplate](/type/HtmlTemplate.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Conv](/type/Conv.md)
- [HtmlTemplate](/type/HtmlTemplate.md)
