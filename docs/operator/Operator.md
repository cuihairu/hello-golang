# 运算符
Go 的运算符和 C 系语言大体一致，少数几个（如自增自减、没有三元运算符）有自己的取舍。下面按类给出清单和示例代码。

### 1. 算术运算符

算术运算符做加 `+`、减 `-`、乘 `*`、除 `/`、取余 `%`，都是二元运算。

示例代码：
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

### 2. 关系运算符

关系运算符比较两个值，结果是布尔值：`==`、`!=`、`>`、`<`、`>=`、`<=`。

示例代码：
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

### 3. 逻辑运算符

逻辑运算符只有三个：与 `&&`、或 `||`、非 `!`，操作数是布尔值。

示例代码：
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

### 4. 赋值运算符

除了 `=` 直接赋值，`+=`、`-=`、`*=`、`/=`、`%=` 把运算和赋值合成一步，等价于"先算后存"。

示例代码：
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

### 5. 位运算符

位运算符直接操作整数的二进制位：按位与 `&`、按位或 `|`、按位异或 `^`、按位取反 `^`、左移 `<<`、右移 `>>`。注意 `^` 有两个身份：双目时是异或，单目时是取反。

示例代码：
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

### 6. 条件运算符（Go 不直接支持三元运算符）

Go 语言没有直接的条件运算符（如 `? :`），但可以使用 `if` 语句来实现类似的功能。

示例代码：
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

### 7. 自增和自减运算符

自增 `++` 和自减 `--` 把变量的值加一或减一。它们是语句而不是表达式，没有 `++a` 这种前置写法，也不能嵌进别的表达式里。

示例代码：
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

### 总结

上面七类里，Go 与其他语言差别最明显的是两处：整数除法 `/` 直接截断小数（`10 / 3` 得 `3`），以及没有三元运算符，条件取值只能写 `if`。自增自减只能单独成句，这也是为什么 `for i := 0; i < n; i++` 里它们放在后置位置。