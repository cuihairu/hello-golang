# range
在 Go 语言中，`range` 是一个用于迭代各种数据结构的关键字。它可以用来遍历数组、切片、映射（map）、字符串以及通道（channel）。`range` 使得在这些数据结构上进行迭代变得非常简单和直接。

### 基本用法

`range` 关键字用于 `for` 循环中，可以迭代各种类型的数据结构。每次迭代，`range` 返回一个或多个值，具体取决于数据结构的类型。

#### 示例：迭代数组和切片

```go
package main

import "fmt"

func main() {
    // 迭代数组
    arr := [3]int{1, 2, 3}
    for index, value := range arr {
        fmt.Printf("Index: %d, Value: %d\n", index, value)
    }

    // 迭代切片
    slice := []int{4, 5, 6}
    for index, value := range slice {
        fmt.Printf("Index: %d, Value: %d\n", index, value)
    }
}
```

**输出：**

```
Index: 0, Value: 1
Index: 1, Value: 2
Index: 2, Value: 3
Index: 0, Value: 4
Index: 1, Value: 5
Index: 2, Value: 6
```

#### 示例：迭代映射（Map）

```go
package main

import "fmt"

func main() {
    // 迭代映射
    m := map[string]int{"a": 1, "b": 2, "c": 3}
    for key, value := range m {
        fmt.Printf("Key: %s, Value: %d\n", key, value)
    }
}
```

**输出：**

```
Key: a, Value: 1
Key: b, Value: 2
Key: c, Value: 3
```

#### 示例：迭代字符串

```go
package main

import "fmt"

func main() {
    // 迭代字符串
    s := "hello"
    for index, char := range s {
        fmt.Printf("Index: %d, Rune: %c\n", index, char)
    }
}
```

**输出：**

```
Index: 0, Rune: h
Index: 1, Rune: e
Index: 2, Rune: l
Index: 3, Rune: l
Index: 4, Rune: o
```

#### 示例：迭代通道（Channel）

```go
package main

import "fmt"

func main() {
    ch := make(chan int)

    // 启动一个 goroutine 发送数据到通道
    go func() {
        for i := 0; i < 3; i++ {
            ch <- i
        }
        close(ch)
    }()

    // 迭代通道
    for value := range ch {
        fmt.Println("Received:", value)
    }
}
```

**输出：**

```
Received: 0
Received: 1
Received: 2
```

### `range` 的工作机制

- **数组和切片**：`range` 返回两个值：索引和对应的元素值。迭代时，`range` 会复制数组或切片的元素，所以如果需要修改元素值，通常需要直接操作索引。
  
- **映射（Map）**：`range` 返回两个值：键和对应的值。键值对的遍历顺序是无序的，因为映射本身是无序的。

- **字符串**：`range` 返回两个值：索引和字符（rune）。字符是 Unicode 码点，`range` 会按字符遍历字符串，即使字符是多个字节。

- **通道（Channel）**：`range` 从通道中接收数据直到通道被关闭。关闭通道时，`range` 循环会终止。

### 总结

- `range` 是一个强大的工具，用于在 Go 中迭代数组、切片、映射、字符串和通道。
- 对于数组和切片，`range` 返回索引和值。
- 对于映射，`range` 返回键和值。
- 对于字符串，`range` 返回索引和字符（rune）。
- 对于通道，`range` 遍历直到通道被关闭。

通过使用 `range`，Go 语言的开发者可以编写更简洁和可读的代码来处理各种数据结构的迭代。