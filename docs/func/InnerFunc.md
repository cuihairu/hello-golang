# Go内置函数
Go 语言内置函数（built-in functions）是 Go 语言标准库提供的一组函数，这些函数是语言的一部分，无需显式导入。内置函数在 Go 的各种编程任务中非常实用，包括基本的类型转换、操作、和常见的语言特性。

以下是 Go 的主要内置函数及其参数说明：

### 1. `append`

**功能**：向切片添加元素并返回新的切片。

**参数**：
- `s`：切片。
- `elem`：要添加的元素，可以是一个或多个。

**返回值**：返回包含添加元素的新切片。

**示例**：

```go
package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    s = append(s, 4, 5)
    fmt.Println(s) // 输出： [1 2 3 4 5]
}
```

### 2. `cap`

**功能**：返回切片、数组或通道的容量。

**参数**：
- `v`：切片、数组或通道。

**返回值**：返回容量的整数值。

**示例**：

```go
package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    fmt.Println(cap(s)) // 输出： 3
}
```

### 3. `close`

**功能**：关闭通道，通知接收方没有更多数据将被发送。

**参数**：
- `c`：要关闭的通道。

**返回值**：无。

**示例**：

```go
package main

import "fmt"

func main() {
    ch := make(chan int)
    go func() {
        for i := 0; i < 3; i++ {
            ch <- i
        }
        close(ch)
    }()

    for value := range ch {
        fmt.Println(value)
    }
}
```

### 4. `copy`

**功能**：将源切片的元素复制到目标切片中。

**参数**：
- `dst`：目标切片。
- `src`：源切片。

**返回值**：返回实际复制的元素数量。

**示例**：

```go
package main

import "fmt"

func main() {
    src := []int{1, 2, 3}
    dst := make([]int, len(src))
    n := copy(dst, src)
    fmt.Println(dst) // 输出： [1 2 3]
    fmt.Println(n)   // 输出： 3
}
```

### 5. `delete`

**功能**：从映射中删除键值对。

**参数**：
- `m`：映射。
- `key`：要删除的键。

**返回值**：无。

**示例**：

```go
package main

import "fmt"

func main() {
    m := map[string]int{"a": 1, "b": 2}
    delete(m, "b")
    fmt.Println(m) // 输出： map[a:1]
}
```

### 6. `len`

**功能**：返回切片、数组、映射或字符串的长度。

**参数**：
- `v`：切片、数组、映射或字符串。

**返回值**：返回长度的整数值。

**示例**：

```go
package main

import "fmt"

func main() {
    s := []int{1, 2, 3}
    fmt.Println(len(s)) // 输出： 3

    m := map[string]int{"a": 1, "b": 2}
    fmt.Println(len(m)) // 输出： 2

    str := "hello"
    fmt.Println(len(str)) // 输出： 5
}
```

### 7. `make`

**功能**：创建切片、映射或通道，并初始化它们。

**参数**：
- `t`：要创建的类型（`slice`, `map`, `channel`）。
- `len`：（对于切片和映射）初始长度。
- `cap`：（对于切片）容量。

**返回值**：返回新创建的切片、映射或通道。

**示例**：

```go
package main

import "fmt"

func main() {
    // 创建切片
    s := make([]int, 3, 5)
    fmt.Println(s) // 输出： [0 0 0]
    fmt.Println(cap(s)) // 输出： 5

    // 创建映射
    m := make(map[string]int)
    m["a"] = 1
    fmt.Println(m) // 输出： map[a:1]

    // 创建通道
    ch := make(chan int, 2)
    ch <- 1
    ch <- 2
    fmt.Println(<-ch) // 输出： 1
}
```

### 8. `new`

**功能**：分配内存并初始化为零值，返回指向该内存的指针。

**参数**：
- `t`：要创建的类型。

**返回值**：返回指向新分配内存的指针。

**示例**：

```go
package main

import "fmt"

func main() {
    // 创建 int 类型的零值
    p := new(int)
    fmt.Println(*p) // 输出： 0
}
```

### 9. `panic`

**功能**：引发运行时错误，程序将停止执行并调用 `defer` 中的清理函数。

**参数**：
- `v`：要引发的错误值。

**返回值**：无。

**示例**：

```go
package main

import "fmt"

func main() {
    defer fmt.Println("Defer executed")
    panic("Something went wrong")
}
```

### 10. `recover`

**功能**：从 `panic` 中恢复，允许程序继续执行。

**参数**：
- 无。

**返回值**：返回传递给 `panic` 的值，如果没有 `panic`，返回 `nil`。

**示例**：

```go
package main

import "fmt"

func safeDivision(a, b int) (result int) {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("Recovered from panic:", r)
        }
    }()
    if b == 0 {
        panic("Division by zero")
    }
    return a / b
}

func main() {
    fmt.Println(safeDivision(10, 2)) // 输出： 5
    fmt.Println(safeDivision(10, 0)) // 输出： Recovered from panic: Division by zero
}
```

### 总结

- **`append`**：向切片添加元素。
- **`cap`**：返回切片、数组或通道的容量。
- **`close`**：关闭通道。
- **`copy`**：将源切片的元素复制到目标切片。
- **`delete`**：从映射中删除键值对。
- **`len`**：返回切片、数组、映射或字符串的长度。
- **`make`**：创建并初始化切片、映射或通道。
- **`new`**：分配内存并初始化为零值，返回指针。
- **`panic`**：引发运行时错误。
- **`recover`**：从 `panic` 中恢复。

这些内置函数提供了强大的功能，帮助 Go 程序员在编写代码时更高效地处理各种任务。