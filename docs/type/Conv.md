在 Go 语言中，类型转换是一种将一个类型的值显式地转换为另一个类型的过程。由于 Go 是一种强类型语言，它不会自动进行隐式类型转换，因此需要显式地进行类型转换。类型转换通常用于不同基本类型之间的转换，如整数、浮点数、字符串和布尔值等。

### 基本类型转换的常见场景

1. **整数类型之间的转换**：
   整数类型包括 `int`, `int8`, `int16`, `int32`, `int64` 以及它们的无符号版本 `uint`, `uint8`, `uint16`, `uint32`, `uint64`。你可以通过显式类型转换在这些类型之间进行转换。

   ```go
   var a int = 100
   var b int32 = int32(a)
   var c int64 = int64(a)
   var d uint = uint(a)
   ```

2. **整数和浮点数之间的转换**：
   将整数转换为浮点数或将浮点数转换为整数需要显式进行，通常用于需要进行不同精度计算的场景。

   ```go
   var a int = 42
   var b float64 = float64(a)
   var c int = int(b)
   ```

3. **字符串和其他基本类型之间的转换**：
   Go 提供了 `strconv` 包来处理字符串和其他基本类型之间的转换，如将字符串转换为整数、浮点数或布尔值，反之亦然。

   ```go
   import "strconv"
   
   var s string = "123"
   n, err := strconv.Atoi(s)

   var f float64 = 3.14
   var str string = strconv.FormatFloat(f, 'f', -1, 64)
   ```

4. **布尔类型和字符串之间的转换**：
   可以使用 `strconv` 包将布尔值转换为字符串或从字符串解析布尔值。

   ```go
   var s string = "true"
   b, err := strconv.ParseBool(s)
   
   var boolVal bool = true
   var strBool string = strconv.FormatBool(boolVal)
   ```

### 类型转换的注意事项

1. **显式进行**：类型转换在 Go 中需要显式进行，不能依赖隐式转换。
2. **可能的精度丢失**：在整数和浮点数之间转换时，可能会出现精度丢失。例如，将浮点数转换为整数会丢弃小数部分。
3. **错误处理**：在字符串和其他基本类型之间转换时，可能会出现解析错误，需要进行错误处理。

### 示例代码

```go
package main

import (
    "fmt"
    "strconv"
)

func main() {
    var a int = 42
    var b float64 = float64(a) // 整数转换为浮点数
    var c int = int(b)         // 浮点数转换为整数

    fmt.Println(b) // 输出: 42.0
    fmt.Println(c) // 输出: 42

    var s string = "123"
    n, err := strconv.Atoi(s)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(n) // 输出: 123
    }

    var boolStr string = "true"
    boolVal, err := strconv.ParseBool(boolStr)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(boolVal) // 输出: true
    }

    var numStr string = strconv.Itoa(456)
    fmt.Println(numStr) // 输出: "456"
}
```

通过显式类型转换，Go 程序能够保持类型安全性，减少潜在的类型错误，同时也增加了代码的可读性和维护性。