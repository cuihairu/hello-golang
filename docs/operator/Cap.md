在 Go 语言中，**容量运算符**（capacity operator）并不是一个单独的运算符，而是通过内置函数 `cap` 来获取集合类型（如切片、数组、通道）的容量。

### 1. **容量（Capacity）的概念**

- **容量**指的是集合类型在不重新分配内存的情况下，能够存储的最大元素数量。对于切片和数组，容量是从切片或数组的起始位置到其底层数组的末尾的长度。

### 2. **使用 `cap` 函数获取容量**

- **切片（slice）**：`cap` 函数返回切片的容量，即底层数组从切片的起始位置到数组末尾的长度。
- **数组（array）**：`cap` 函数返回数组的长度和容量，这两个值是相同的。
- **通道（channel）**：`cap` 函数返回通道的缓冲区容量，即通道可以缓存的最大元素数量。

### 示例代码

#### 切片的容量

```go
package main

import "fmt"

func main() {
    s := make([]int, 5, 10) // 创建一个长度为5、容量为10的切片
    fmt.Println("Slice:", s)
    fmt.Println("Length:", len(s))
    fmt.Println("Capacity:", cap(s)) // 输出: Capacity: 10
}
```

在这个示例中，`cap(s)` 返回 10，因为切片 `s` 的容量为 10。

#### 数组的容量

```go
package main

import "fmt"

func main() {
    a := [5]int{1, 2, 3, 4, 5}
    fmt.Println("Array:", a)
    fmt.Println("Length:", len(a))
    fmt.Println("Capacity:", cap(a)) // 输出: Capacity: 5
}
```

在这个示例中，`cap(a)` 返回 5，因为数组 `a` 的长度和容量都是 5。

#### 通道的容量

```go
package main

import "fmt"

func main() {
    c := make(chan int, 5) // 创建一个缓冲区容量为5的通道
    fmt.Println("Channel capacity:", cap(c)) // 输出: Channel capacity: 5
}
```

在这个示例中，`cap(c)` 返回 5，因为通道 `c` 的缓冲区容量为 5。

### 总结

- **容量** 是集合在不重新分配内存的情况下能够存储的最大元素数量。
- **Go 使用 `cap` 函数** 获取切片、数组和通道的容量：
  - **切片**：`cap(slice)` 返回切片的容量。
  - **数组**：`cap(array)` 返回数组的长度和容量（两者相同）。
  - **通道**：`cap(channel)` 返回通道缓冲区的容量。

判断切片会不会触发扩容时，`len` 和 `cap` 要一起看：`len` 是已存元素个数，`cap` 是不重新分配内存就能装下的数量。