Go provides a rich set of basic types, including integer types, floating-point types, string types, and boolean types. In the course of programming, you often need to convert between different basic types. Go is a strongly typed language and does not perform implicit conversions automatically, so conversions must be done explicitly.

### Conversions Between Integer Types

Integer types include `int`, `int8`, `int16`, `int32`, `int64`, and their corresponding unsigned types `uint`, `uint8`, `uint16`, `uint32`, `uint64`. You can explicitly convert between different integer types:

```go
package main

import (
	"fmt"
)

func main() {
	var a int = 100
	var b int32 = int32(a)
	var c int64 = int64(a)
	var d uint = uint(a)

	fmt.Println(b) // prints: 100
	fmt.Println(c) // prints: 100
	fmt.Println(d) // prints: 100
}
```

### Conversions Between Integers and Floating-Point Numbers

Conversions between integers and floating-point numbers must be done explicitly:

```go
package main

import (
	"fmt"
)

func main() {
	var a int = 42
	var b float64 = float64(a) // integer to floating point
	var c int = int(b)         // floating point to integer

	fmt.Println(b) // prints: 42.0
	fmt.Println(c) // prints: 42
}
```

### Conversions Between Strings and Other Basic Types

Go provides the standard library `strconv` for conversions between strings and other basic types.

#### String to Integer

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var s string = "123"
	n, err := strconv.Atoi(s)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(n) // prints: 123
	}
}
```

#### Integer to String

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var n int = 456
	var s string = strconv.Itoa(n)
	fmt.Println(s) // prints: "456"
}
```

#### String to Floating Point

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var s string = "3.14"
	f, err := strconv.ParseFloat(s, 64)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(f) // prints: 3.14
	}
}
```

#### Floating Point to String

```go
package main

import (
	"fmt"
)

func main() {
	var f float64 = 1.618
	var s string = fmt.Sprintf("%f", f)
	fmt.Println(s) // prints: "1.618000"
}
```

### Conversions Between Booleans and Strings

#### String to Boolean

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var s string = "true"
	b, err := strconv.ParseBool(s)
	if err != nil {
		fmt.Println(err)
	} else {
		fmt.Println(b) // prints: true
	}
}
```

#### Boolean to String

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	var b bool = true
	var s string = strconv.FormatBool(b)
	fmt.Println(s) // prints: "true"
}
```

### Notes

1. **Conversions must be explicit**: Go does not perform implicit conversions automatically.
2. **Possible precision loss**: during conversion, especially between floating-point and integer types, precision may be lost.
3. **Error handling**: conversions between strings and other basic types can encounter errors, which need to be handled.

The cost of explicit conversion is writing the target type at every conversion site; the benefit is that problems are easy to locate: converting a float to an int drops the fractional part, and widening a narrow integer to a wider one can overflow, and neither is a compile error — you only get a "wrong" number at run time. When you write a conversion, a quick look at the width of both sides saves you from debugging later.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Conversions](https://go.dev/ref/spec#Conversions)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [Big](/type/Big.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Big](/type/Big.md)
