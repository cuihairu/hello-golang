## 声明

在 Go 语言中，声明（declaration）是定义变量、常量、类型和函数等元素的过程。声明是程序的基本组成部分，正确理解和使用声明是编写 Go 程序的基础。本节将详细介绍 Go 语言中的各种声明，并提供相关示例。

### 变量声明

变量声明用于定义程序中的变量。Go 语言提供了多种声明变量的方式。

#### 1. 使用 `var` 关键字声明变量

使用 `var` 关键字可以显式声明变量，并为其指定类型和初始值。

```go
package main

import "fmt"

func main() {
    // 声明一个整型变量并赋初始值
    var i int = 10
    fmt.Println(i)

    // 声明一个字符串变量，使用默认初始值（空字符串）
    var s string
    fmt.Println(s)

    // 声明一个布尔变量并赋初始值
    var b bool = true
    fmt.Println(b)
}
```

#### 2. 简短变量声明

简短变量声明使用 `:=` 语法，可以在函数内部声明变量，并根据初始值自动推断类型。

```go
package main

import "fmt"

func main() {
    // 声明并初始化整型变量
    i := 10
    fmt.Println(i)

    // 声明并初始化字符串变量
    s := "Hello, Go"
    fmt.Println(s)

    // 声明并初始化布尔变量
    b := true
    fmt.Println(b)
}
```

#### 3. 多变量声明

可以同时声明多个变量，使用 `var` 关键字或简短声明语法。

```go
package main

import "fmt"

func main() {
    // 使用 var 关键字声明多个变量
    var x, y, z int = 1, 2, 3
    fmt.Println(x, y, z)

    // 使用简短声明语法声明多个变量
    a, b, c := 4, "Go", false
    fmt.Println(a, b, c)
}
```

### 常量声明

常量声明使用 `const` 关键字，定义在程序执行期间其值不会改变的变量。常量可以是数字、字符串或布尔类型。

```go
package main

import "fmt"

func main() {
    // 声明整数常量
    const Pi = 3.14
    fmt.Println(Pi)

    // 声明字符串常量
    const Greeting = "Hello, Go"
    fmt.Println(Greeting)

    // 声明布尔常量
    const IsGoAwesome = true
    fmt.Println(IsGoAwesome)
}
```

#### 使用 `iota` 枚举常量

`iota` 是一个特殊的常量生成器，可以用来简化一系列相关常量的定义。每遇到一个 `const` 关键字，`iota` 的值就会从 0 开始，每定义一个常量 `iota` 的值就会自动递增。

```go
package main

import "fmt"

// 使用 iota 定义枚举常量
const (
    Sunday = iota
    Monday
    Tuesday
    Wednesday
    Thursday
    Friday
    Saturday
)

func main() {
    fmt.Println(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) // 输出 0 1 2 3 4 5 6
}
```

### 类型声明

类型声明使用 `type` 关键字，定义新的类型名称（类型别名）或自定义类型。类型声明可以使代码更具可读性和可维护性。

#### 1. 类型别名

类型别名为已有类型定义新的名称。

```go
package main

import "fmt"

// 定义类型别名
type MyString string

func main() {
    var s MyString = "Hello, Go"
    fmt.Println(s)
}
```

#### 2. 自定义类型

自定义类型用于定义结构体、接口等复杂类型。

```go
package main

import "fmt"

// 定义结构体类型
type Person struct {
    Name string
    Age  int
}

// 定义接口类型
type Describer interface {
    Describe() string
}

func main() {
    p := Person{Name: "Alice", Age: 30}
    fmt.Println(p)
}
```

#### 3. 函数类型

函数类型用于定义具有相同签名的函数集合。

```go
package main

import "fmt"

// 定义函数类型
type MathOperation func(int, int) int

// 定义加法操作
func add(a, b int) int {
    return a + b
}

// 定义减法操作
func subtract(a, b int) int {
    return a - b
}

func main() {
    // 声明一个函数类型变量并赋值
    var op MathOperation

    // 使用加法操作
    op = add
    fmt.Println("Addition:", op(3, 4)) // 输出 7

    // 使用减法操作
    op = subtract
    fmt.Println("Subtraction:", op(3, 4)) // 输出 -1
}
```

### 函数声明

函数声明使用 `func` 关键字，定义具有特定功能的代码块。函数可以有参数和返回值。

```go
package main

import "fmt"

// 定义无参无返回值函数
func sayHello() {
    fmt.Println("Hello, Go")
}

// 定义有参数的函数
func add(a int, b int) int {
    return a + b
}

// 定义多返回值的函数
func swap(x, y string) (string, string) {
    return y, x
}

func main() {
    sayHello()
    
    sum := add(3, 4)
    fmt.Println("Sum:", sum)

    a, b := swap("first", "second")
    fmt.Println("Swapped:", a, b)
}
```

### 全局声明

全局声明的变量、常量或类型在整个包中都可以访问和使用。这些声明通常位于包级别（函数体外），在包的任意位置都可以使用。

```go
package main

import "fmt"

// 全局变量声明
var GlobalVar = "I am a global variable"

// 全局常量声明
const GlobalConst = "I am a global constant"

// 全局类型声明
type GlobalType struct {
    name string
    age  int
}

func main() {
    // 使用全局变量
    fmt.Println(GlobalVar)

    // 使用全局常量
    fmt.Println(GlobalConst)

    // 使用全局类型
    g := GlobalType{name: "Alice", age: 30}
    fmt.Println(g)
}
```

### 变量作用域

变量的作用域（scope）决定了它可以被访问的范围。变量作用域包括包作用域、函数作用域和块作用域。

#### 1. 包作用域

包作用域的变量在整个包中都可访问。

```go
package main

import "fmt"

// 包作用域变量
var packageVar = "I am at package level"

func main() {
    fmt.Println(packageVar)
}
```

#### 2. 函数作用域

函数作用域的变量仅在函数内可访问。

```go
package main

import "fmt"

func main() {
    // 函数作用域变量
    var funcVar = "I am at function level"
    fmt.Println(funcVar)
}
```

#### 3. 块作用域

块作用域的变量仅在块内可访问，块由 `{}` 定义。

```go
package main

import "fmt"

func main() {
    if true {
        // 块作用域变量
        var blockVar = "I am at block level"
        fmt.Println(blockVar)
    }
    // fmt.Println(blockVar) // 错误：块作用域外无法访问 blockVar
}
```

