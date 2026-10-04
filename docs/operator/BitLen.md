Go 没有 `bit length` 运算符（有些语言有）。位长度指表示该整数所需的二进制位数。

### 计算位长度

Go 里两种做法：调 `bits.Len`，或者自己写个右移计数。

#### 1. 使用 `math/bits` 包

`math/bits` 包的 `bits.Len` 直接给出无符号整数的位长度。

```go
package main

import (
    "fmt"
    "math/bits"
)

func main() {
    num := 23  // 二进制: 10111
    bitLength := bits.Len(uint(num))
    fmt.Println("Bit length of", num, "is:", bitLength) // 输出: Bit length of 23 is: 5
}
```

在这个示例中，`bits.Len` 函数计算了无符号整数的位长度。对于有符号整数，你需要先将其转换为无符号整数（例如使用 `uint` 类型）。

#### 2. 手动计算

手写的做法是反复右移，每移一位计数加一：

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
    num := 23  // 二进制: 10111
    bitLength := bitLength(num)
    fmt.Println("Bit length of", num, "is:", bitLength) // 输出: Bit length of 23 is: 5
}
```

数字右移到 0，计数器的值就是位长度；`n == 0` 单独返回 1。

### 总结

- Go 语言本身没有直接的位长度运算符。
- 你可以使用 `math/bits` 包中的 `bits.Len` 函数来计算无符号整数的位长度。
- 也可以手动实现计算函数来获得整数的位长度，适用于各种整数类型。