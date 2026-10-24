In Go, integer types are a kind of data type used to represent integers. Go provides several integer types, each with a different size and range, suited to different use cases.

### Integer Types in Go

The following are the main integer types in Go and their ranges:

- `int8`: 8-bit signed integer, range -128 to 127.
- `int16`: 16-bit signed integer, range -32768 to 32767.
- `int32`: 32-bit signed integer, range -2147483648 to 2147483647.
- `int64`: 64-bit signed integer, range -9223372036854775808 to 9223372036854775807.
- `int`: the exact size depends on the compiler, usually 32 or 64 bits.
- `uint8`: 8-bit unsigned integer, range 0 to 255.
- `uint16`: 16-bit unsigned integer, range 0 to 65535.
- `uint32`: 32-bit unsigned integer, range 0 to 4294967295.
- `uint64`: 64-bit unsigned integer, range 0 to 18446744073709551615.
- `uint`: the exact size depends on the compiler, usually 32 or 64 bits.

### Use Cases

Integer types of different sizes suit different data ranges and scenarios:

1. **Choosing standard-sized integers (`int` and `uint`)**:
   - Using `int` or `uint` guarantees you get the fastest integer size the compiler supports in most cases.
   - Suitable for general integer arithmetic and indexing into data structures, such as array indexes and loop counters.

   ```go
   var count int = 100
   fmt.Println(count)
   ```

2. **When you need a specific size (`int8`, `int16`, etc.)**:
   - When you know the data range or memory constraints for certain, you can pick a smaller integer type to save memory.
   - For example, when handling file bytes or buffer sizes, you might use `int8` or `uint16`.

   ```go
   var buffer [1024]uint8
   fmt.Println(len(buffer))
   ```

3. **Unsigned integers (the `uint` family)**:
   - When handling bitwise operations, unsigned data, or cases that only need non-negative numbers, use unsigned integer types.
   - For example, when dealing with binary data in files or packet sizes in network communication.

   ```go
   var packetSize uint32 = 1024
   fmt.Println(packetSize)
   ```

4. **Large integers (`int64` and `uint64`)**:
   - When you need to handle a large range of integers or involve large amounts of data, choose `int64` or `uint64`.
   - For example, when handling timestamps, large file sizes, or counters in a database.

   ```go
   var fileSize int64 = 2147483648
   fmt.Println(fileSize)
   ```

### Notes

- **Performance and memory**: choosing the appropriate integer type can improve program performance and save memory.
- **Type conversion**: between integer types of different sizes you need explicit type conversion to make sure data is not lost or overflowing.

```go
var x int32 = 100
var y int64 = int64(x)
```

Writing plain `int` by default is enough; when you run into binary protocols, file formats, or memory-sensitive scenarios, then pick a sized type according to the data range.

### Overflow

In Go, integer overflow is something you need to pay special attention to. Overflow happens when the result of an integer computation goes beyond the range its type can represent. Go handles overflow differently depending on whether the integer is signed or unsigned.

### Signed Integer Overflow

For signed integer types (such as `int8`, `int16`, `int32`, `int64`, and `int`), overflow pushes the result beyond the type's range, which can lead to unexpected results.

```go
package main

import "fmt"

func main() {
    var x int8 = 127
    x = x + 1 // overflow, the result is -128
    fmt.Println(x)
}
```

In the example above, the range of `int8` is `-128` to `127`; when `x` is `127`, adding `1` causes overflow and `x` becomes `-128`.

### Unsigned Integer Overflow

For unsigned integer types (such as `uint8`, `uint16`, `uint32`, `uint64`, and `uint`), overflow pushes the result beyond the type's range, and in that case the value wraps around to the minimum value of the type.

```go
package main

import "fmt"

func main() {
    var y uint8 = 255
    y = y + 1 // overflow, the result is 0
    fmt.Println(y)
}
```

In the example above, the range of `uint8` is `0` to `255`; when `y` is `255`, adding `1` causes overflow and `y` becomes `0`.

### Impact of Overflow and Handling

Overflow can lead to undefined behavior or wrong results at run time. To avoid problems caused by overflow, you can take the following measures:

1. **Use an integer of appropriate size**: choose an integer type large enough to hold the expected value and avoid overflow.

2. **Check boundary conditions**: before an operation that could overflow, check the value range to avoid exceeding what the type can represent.

3. **Use extra logic**: when handling scenarios that could overflow, consider using conditional statements or other logic to keep the operation safe.

4. **Handle overflow explicitly**: for addition and subtraction of unsigned integers you can use functions like `Add`, `Add32`, `Add64` from the standard library `math/bits` package, which signal overflow through an extra carry/borrow return value; signed integers have no corresponding library functions, so you need to compare values before and after the operation or estimate the bounds to tell.

```go
package main

import (
    "fmt"
    "math/bits"
)

func main() {
    var x uint32 = 4294967295 // 2^32 - 1
    sum, carry := bits.Add32(x, 1, 0)
    if carry == 1 {
        // handle the overflow case
    }
    fmt.Println("sum:", sum, "carry:", carry)
}
```

Estimate the bounds before you add, subtract, or multiply: `int8` past 127 wraps to -128, and `uint8` past 255 wraps to 0 — both wraps are defined, deterministic behavior in Go.

## References

- [Language Specification · Types](https://go.dev/ref/spec#Types)
- [Language Specification · Numeric Types](https://go.dev/ref/spec#Numeric_types)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [HtmlTemplate](/type/HtmlTemplate.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [HtmlTemplate](/type/HtmlTemplate.md)
