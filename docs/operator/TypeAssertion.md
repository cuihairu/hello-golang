类型断言（Type Assertion）在运行时检查接口变量里存的到底是哪个具体类型，并把值取出来。

### 类型断言的基本语法

基本语法：

```go
value, ok := interface.(T)
```

- **`interface`** 是要断言的接口类型。
- **`T`** 是要断言的具体类型。
- **`value`** 是断言成功时的具体类型值。
- **`ok`** 是一个布尔值，表示断言是否成功。

### 类型断言的两种形式

1. **成功断言（带有返回值）**

   ```go
   var i interface{} = "hello"
   s, ok := i.(string)
   if ok {
       fmt.Println("String value:", s)
   } else {
       fmt.Println("Not a string")
   }
   ```

   `ok` 告诉你断言有没有成功，`s` 是成功后拿到的那个具体值。

2. **直接断言（不带返回值）**

   ```go
   var i interface{} = "hello"
   s := i.(string)
   fmt.Println("String value:", s)
   ```

   这种形式直接取值，断言失败会 panic。拿不准类型时，用带返回值的那种更稳妥。

### 示例代码

#### 示例 1: 断言成功

```go
package main

import "fmt"

func main() {
    var i interface{} = 42
    value, ok := i.(int)
    if ok {
        fmt.Println("The value is an int:", value)
    } else {
        fmt.Println("The value is not an int")
    }
}
```

#### 示例 2: 断言失败

```go
package main

import "fmt"

func main() {
    var i interface{} = "hello"
    value, ok := i.(int)
    if ok {
        fmt.Println("The value is an int:", value)
    } else {
        fmt.Println("The value is not an int")
    }
}
```

### 空接口的类型断言

空接口 `interface{}` 可以持有任何类型的值。当你需要将空接口的值转换为具体类型时，可以使用类型断言：

```go
package main

import "fmt"

func printValue(v interface{}) {
    switch v := v.(type) {
    case int:
        fmt.Println("Integer:", v)
    case string:
        fmt.Println("String:", v)
    default:
        fmt.Println("Unknown type")
    }
}

func main() {
    printValue(10)       // 输出: Integer: 10
    printValue("hello")  // 输出: String: hello
    printValue(3.14)     // 输出: Unknown type
}
```

### 总结

- **类型断言** 允许你在运行时检查接口变量的实际类型，并将其转换为该类型。
- **带返回值的断言** 允许你安全地检查断言是否成功，避免运行时错误。
- **直接断言** 不返回成功标志，但断言失败时会导致运行时错误。
- **空接口** 可以持有任何类型的值，类型断言在处理空接口时尤其有用。

三种写法各管一段：知道类型一定对就直接断言，拿不准就带 `ok` 判断，多个类型挨个分支则用 `switch v := v.(type)`。