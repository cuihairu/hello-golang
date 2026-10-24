Go has two built-in complex types, `complex64` and `complex128`. Computations such as Fourier transforms, signal processing, and control theory make use of them.

### Definition of the complex types

1. **`complex64`**: represents a complex number made of two `float32` values; both the real and imaginary parts are `float32`.
2. **`complex128`**: represents a complex number made of two `float64` values; both the real and imaginary parts are `float64`.

### Creating and initializing complex numbers

A complex number can be created with the built-in `complex` function, or by direct assignment.

#### Using the `complex` function

```go
var c1 complex64 = complex(1.0, 2.0)  // real part 1.0, imaginary part 2.0
var c2 complex128 = complex(3.0, 4.0) // real part 3.0, imaginary part 4.0
```

#### Direct assignment

```go
var c3 complex64 = 1.0 + 2.0i
var c4 complex128 = 3.0 + 4.0i
```

### Operations on complex numbers

Go provides the basic operations on complex numbers: addition, subtraction, multiplication, and division.

```go
package main

import (
	"fmt"
)

func main() {
	c1 := complex(1.0, 2.0)
	c2 := complex(3.0, 4.0)

	// complex addition
	cAdd := c1 + c2
	fmt.Printf("Addition: %v\n", cAdd)

	// complex subtraction
	cSub := c1 - c2
	fmt.Printf("Subtraction: %v\n", cSub)

	// complex multiplication
	cMul := c1 * c2
	fmt.Printf("Multiplication: %v\n", cMul)

	// complex division
	cDiv := c1 / c2
	fmt.Printf("Division: %v\n", cDiv)
}
```

### Getting the real and imaginary parts

The `real` and `imag` functions retrieve the real and imaginary parts of a complex number.

```go
package main

import (
	"fmt"
)

func main() {
	c := complex(1.0, 2.0)

	// get the real part
	realPart := real(c)
	fmt.Printf("Real part: %v\n", realPart)

	// get the imaginary part
	imagPart := imag(c)
	fmt.Printf("Imaginary part: %v\n", imagPart)
}
```

### Use cases for complex numbers

1. **Signal processing**: in digital signal processing (DSP), complex numbers are used to represent and process signals.
2. **Fourier transforms**: in the fast Fourier transform (FFT), complex numbers are used to convert a signal from the time domain to the frequency domain.
3. **Control systems**: in control theory, complex numbers are used to analyze and design control systems.
4. **Electromagnetism**: in electromagnetism, complex numbers are used to represent electromagnetic waves and analyze circuits.

### Notes

- **Choice of precision**: choose between `complex64` and `complex128` depending on the precision you need. `complex64` uses less memory but has lower precision; `complex128` has higher precision but uses more memory.
- **Performance considerations**: complex arithmetic may perform worse than real arithmetic, because complex operations involve more computation steps.

The real and imaginary parts come out via the `real` and `imag` functions, and addition, subtraction, multiplication, and division use the operators directly — the syntax is essentially the same as for real numbers.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Language spec · Numeric types](https://go.dev/ref/spec#Numeric_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Byte](/type/Byte.md)
- [CompositeType](/type/CompositeType.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Byte](/type/Byte.md)
- [CompositeType](/type/CompositeType.md)
