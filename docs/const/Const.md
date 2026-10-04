常量是编译期定死、运行中改不了的值，字面量是直接写在代码里的具体值。两者的写法分开看：

### 常量（Constants）

常量是指程序中固定不变的值，一旦定义后不能被修改。在 Go 中，常量可以是数值、布尔值或字符串等基本类型，它们在编译时就已经确定其值。

#### 定义常量

在 Go 中定义常量使用 `const` 关键字，语法为：

```go
const identifier [type] = value
```

- `identifier` 是常量的名称。
- `[type]` 是可选的类型说明符，可以省略，如果省略则根据赋予的值自动推断类型。
- `value` 是常量的值，必须在编译时能够确定。

例如：
```go
const pi = 3.14159
const maxRetry = 3
const welcomeMessage = "Hello, World!"
```

#### 常量枚举

常量枚举是一种常见的用法，可以简化代码中的重复定义：

```go
const (
    Monday    = 1
    Tuesday   = 2
    Wednesday = 3
    Thursday  = 4
    Friday    = 5
)
```

#### 常量表达式

常量可以通过在声明时进行基本运算得到，例如：

```go
const (
    a = 10
    b = 20
    c = a + b // 常量表达式
)
```

### 字面量（Literals）

字面量是表示固定值的符号，字面量可以是常量、变量或表达式的具体值。在 Go 中，有多种类型的字面量：

- **整数字面量**：如 `42`, `-100`, `0xFF`（十六进制）、`077`（八进制）等。
- **浮点数字面量**：如 `3.14`, `1.5e-10` 等。
- **复数字面量**：如 `3.14i`, `1 + 2i` 等。
- **字符串字面量**：如 `"Hello, World!"`, `` `多行
  字符串` `` 等。
- **布尔字面量**：`true` 和 `false`。
- **符文字面量**：如 `'a'`, `'\n'`, `'\u2318'` 等。

#### 示例

```go
package main

import "fmt"

func main() {
    const pi = 3.14159
    fmt.Println("Pi value is", pi)

    const (
        Monday = 1
        Tuesday = 2
        Wednesday = 3
        Thursday = 4
        Friday = 5
    )
    fmt.Println("Monday is", Monday)
}
```

### 总结

- **常量**用 `const` 声明，运行期间不可修改，程序里不会变的值都该放这里，读代码的人一眼就知道它不会动。
- **字面量**是代码里直接写出的值，像 `42`、`3.14`、`"Hello, World!"` 这样，不需要先声明。
- 常量的值必须在编译期就能算出来，算不出来的写法编译器直接报错，错误不会拖到运行时。