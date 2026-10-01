### Go Slice 介绍

切片（Slice）是 Go 语言中一种非常重要的数据结构。它提供了比数组更灵活和强大的功能，用于处理动态大小的集合。下面是对 Go 切片的详细介绍：

### 1. 基本用法

#### 声明和初始化

```go
// 声明一个空的整型切片
var s []int

// 使用字面量初始化
s := []int{1, 2, 3, 4, 5}

// 使用 make 函数创建一个指定长度和容量的切片
s := make([]int, 5)          // 长度和容量都是 5
s := make([]int, 3, 5)       // 长度是 3，容量是 5
```

#### 操作切片

```go
s := []int{1, 2, 3, 4, 5}
fmt.Println(s)            // 输出: [1 2 3 4 5]

s = append(s, 6, 7)       // 添加元素
fmt.Println(s)            // 输出: [1 2 3 4 5 6 7]

subSlice := s[1:4]        // 切片操作，获取子切片
fmt.Println(subSlice)     // 输出: [2 3 4]
```

### 2. 和数组的区别

- **长度**：数组的长度是固定的，声明时就必须指定；切片的长度是动态的，可以在运行时调整。
- **类型**：数组的类型包含长度信息 `[5]int` 和 `[10]int` 是不同的类型；切片没有长度信息 `[]int` 类型。
- **值类型 vs 引用类型**：数组是值类型，赋值和传递会复制整个数组；切片是引用类型，赋值和传递会共享底层数组。
- **内存分配**：数组的内存是连续的固定大小；切片底层是基于数组的，可以通过扩展容量来增加大小。

### 3. 底层实现

切片在底层是一个结构体，包含三个字段：

- **指针**：指向底层数组的起始地址。
- **长度**：切片的当前长度，即切片包含的元素数。
- **容量**：从切片的起始位置到底层数组末尾的元素数。

```go
type slice struct {
    array unsafe.Pointer
    len   int
    cap   int
}
```

当切片增长超出容量时，Go 运行时会分配一个更大的数组，将原有数组的内容复制到新数组中，再释放旧数组的内存。

### 4. 常见的坑

#### 共享底层数组

切片共享底层数组，因此修改一个切片会影响其他共享同一底层数组的切片。

```go
s := []int{1, 2, 3, 4, 5}
subSlice := s[1:4]
subSlice[0] = 100
fmt.Println(s)           // 输出: [1 100 3 4 5]
```

#### 切片扩容

当切片的容量不足时，append 操作会创建一个新的底层数组，这可能会导致一些难以发现的 bug。

```go
s := []int{1, 2, 3}
t := s
s = append(s, 4)
s[0] = 100
fmt.Println(t)           // 输出: [1 2 3]，未受影响，因为 s 指向了新的底层数组
```

#### 使用 make 时容量不足

使用 `make` 函数创建切片时，确保指定合适的容量，避免频繁的内存重新分配。

```go
s := make([]int, 0, 3)
s = append(s, 1, 2, 3, 4)  // 第四个元素会导致底层数组扩容
```

#### 切片初始化为 nil

未初始化的切片默认为 nil，与空切片不同。使用 `make` 函数可以确保切片不是 nil。

```go
var s []int       // s == nil
if s == nil {
    fmt.Println("s is nil")
}

s = make([]int, 0)  // s != nil
if s != nil {
    fmt.Println("s is not nil")
}
```

### 示例代码

```go
package main

import "fmt"

func main() {
    // 基本用法
    s := []int{1, 2, 3, 4, 5}
    fmt.Println(s)            // 输出: [1 2 3 4 5]

    s = append(s, 6, 7)
    fmt.Println(s)            // 输出: [1 2 3 4 5 6 7]

    subSlice := s[1:4]
    fmt.Println(subSlice)     // 输出: [2 3 4]

    // 底层数组共享
    subSlice[0] = 100
    fmt.Println(s)            // 输出: [1 100 3 4 5 6 7]

    // 切片扩容
    t := s
    s = append(s, 8)
    s[0] = 200
    fmt.Println(t)            // 输出: [1 100 3 4 5 6 7]，未受影响

    // nil 切片 vs 空切片
    var nilSlice []int
    emptySlice := make([]int, 0)
    fmt.Println(nilSlice == nil)  // 输出: true
    fmt.Println(emptySlice == nil)  // 输出: false
}
```

切片是 Go 语言中处理动态数据集合的核心工具，理解其基本用法、底层实现和常见坑，有助于编写更高效和可靠的 Go 代码。