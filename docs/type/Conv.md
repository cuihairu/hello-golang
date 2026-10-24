In Go, type conversion is the process of explicitly converting a value of one type to another type. Because Go is a strongly typed language, it does not perform implicit type conversion, so conversions must be explicit. Type conversion is usually used between different basic types, such as integers, floating-point numbers, strings, and booleans.

### Common scenarios for basic type conversion

1. **Conversions between integer types**:
   Integer types include `int`, `int8`, `int16`, `int32`, `int64`, and their unsigned counterparts `uint`, `uint8`, `uint16`, `uint32`, `uint64`. You can convert between these types with an explicit conversion.

   ```go
   var a int = 100
   var b int32 = int32(a)
   var c int64 = int64(a)
   var d uint = uint(a)
   fmt.Println(b, c, d) // 100 100 100
   ```

2. **Conversions between integers and floating-point numbers**:
   Converting an integer to a floating-point number, or a floating-point number to an integer, must be explicit, and is typically used when computations of different precision are needed.

   ```go
   var a int = 42
   var b float64 = float64(a)
   var c int = int(b)
   fmt.Println(b, c) // 42 42
   ```

3. **Conversions between strings and other basic types**:
   Go provides the `strconv` package for converting between strings and other basic types, such as converting a string to an integer, a floating-point number, or a boolean, and vice versa.

   ```go
   var s string = "123"
   n, err := strconv.Atoi(s)
   fmt.Println(n, err) // 123 <nil>

   var f float64 = 3.14
   var str string = strconv.FormatFloat(f, 'f', -1, 64)
   fmt.Println(str) // 3.14
   ```

4. **Conversions between booleans and strings**:
   The `strconv` package can convert a boolean to a string, or parse a boolean from a string.

   ```go
   var s string = "true"
   b, err := strconv.ParseBool(s)
   fmt.Println(b, err) // true <nil>
   
   var boolVal bool = true
   var strBool string = strconv.FormatBool(boolVal)
   fmt.Println(strBool) // true
   ```

### Notes on type conversion

1. **Explicit**: in Go, type conversion must be explicit; you cannot rely on implicit conversion.
2. **Possible precision loss**: converting between integers and floating-point numbers can lose precision. For example, converting a floating-point number to an integer discards the fractional part.
3. **Error handling**: converting between strings and other basic types can produce parsing errors, which need to be handled.

### Example code

```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    var a int = 42
    var b float64 = float64(a) // integer to floating-point
    var c int = int(b)         // floating-point to integer

    fmt.Println(b) // prints: 42.0
    fmt.Println(c) // prints: 42

    var s string = "123"
    n, err := strconv.Atoi(s)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(n) // prints: 123
    }

    var boolStr string = "true"
    boolVal, err := strconv.ParseBool(boolStr)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(boolVal) // prints: true
    }

    var numStr string = strconv.Itoa(456)
    fmt.Println(numStr) // prints: "456"
}
```

To sum up: converting between types uses `TypeName(value)` explicitly, moving in and out of strings uses `strconv`, and functions like `Atoi` and `ParseBool` all return an error, which you have to catch.

## References

- [Language spec · Types](https://go.dev/ref/spec#Types)
- [Language spec · Conversions](https://go.dev/ref/spec#Conversions)


## Sibling pages

- [Assertion](/type/Assertion.md)
- [Interface](/type/Interface.md)
- [Map](/type/Map.md)
- [CompositeType](/type/CompositeType.md)
- [Float](/type/Float.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [CompositeType](/type/CompositeType.md)
- [Float](/type/Float.md)
