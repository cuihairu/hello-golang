# 运算符
在 Go 语言中，运算符的使用也很直观且类似于其他语言。以下是 Go 语言中常见的运算符及其示例代码：

### 1. 算术运算符

算术运算符用于执行基本的数学运算。

- **加法 (`+`)**
- **减法 (`-`)**
- **乘法 (`*`)**
- **除法 (`/`)**
- **取余 (`%`)**

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

关系运算符用于比较两个值，结果是布尔值。

- **等于 (`==`)**
- **不等于 (`!=`)**
- **大于 (`>`)**
- **小于 (`<`)**
- **大于等于 (`>=`)**
- **小于等于 (`<=`)**

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

逻辑运算符用于布尔值的逻辑操作。

- **与 (`&&`)**
- **或 (`||`)**
- **非 (`!`)**

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

赋值运算符用于给变量赋值，或对变量进行计算并赋值。

- **赋值 (`=`)**
- **加赋值 (`+=`)**
- **减赋值 (`-=`)**
- **乘赋值 (`*=`)**
- **除赋值 (`/=`)**
- **取余赋值 (`%=`)**

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

位运算符用于对整数的位进行操作。

- **按位与 (`&`)**
- **按位或 (`|`)**
- **按位异或 (`^`)**
- **按位取反 (`~`)**
- **左移 (`<<`)**
- **右移 (`>>`)**

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
    fmt.Println("~a =", ^a)       // 1010 (inverted bits of 5)
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

用于将变量的值增加或减少 1。

- **自增 (`++`)**
- **自减 (`--`)**

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

运算符在 Go 语言中用于执行各种基本操作，如数学计算、比较、逻辑判断等。熟练掌握这些运算符可以帮助你编写高效且易于理解的代码。