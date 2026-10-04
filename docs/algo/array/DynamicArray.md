# 动态数组
在 Go 语言中，动态数组由切片（`slice`）承担。切片是 Go 中最常用的动态数组实现，长度可随元素增减而变化。

### 切片概述

切片（`slice`）表示一段连续的元素序列，是对底层数组的动态视图，长度和容量都可以在运行时变化。

### 切片的基本概念

1. **切片结构**：
   切片由三部分组成：
   - **指针（`ptr`）**：指向底层数组的起始位置。
   - **长度（`len`）**：切片中包含的元素个数。
   - **容量（`cap`）**：从切片的起始位置到底层数组的末尾的元素个数。

   例如，对于一个长度为 5 的切片，其容量可能是 10，这意味着切片的底层数组可以容纳 10 个元素。

2. **创建切片**：
   - **从数组创建**：
     ```go
     arr := [5]int{1, 2, 3, 4, 5}
     slice := arr[1:4] // 创建一个从数组中切出的切片
     ```
   - **使用 `make` 函数创建**：
     ```go
     slice := make([]int, 3) // 创建一个长度为 3 的切片，容量默认为 3
     slice = make([]int, 3, 5) // 创建一个长度为 3，容量为 5 的切片
     ```
   - **从已有切片创建**：
     ```go
     s1 := []int{1, 2, 3}
     s2 := s1[1:3] // 创建一个从已有切片中切出的切片
     ```

### 切片的操作

1. **访问和修改元素**：
   - 通过索引访问和修改切片中的元素。
   ```go
   slice := []int{10, 20, 30}
   slice[1] = 25 // 修改第二个元素
   fmt.Println(slice[1]) // 输出 25
   ```

2. **切片的扩容**：
   - 当向切片中追加元素时，如果切片的容量不足，Go 会自动扩容底层数组。
   ```go
   slice := []int{1, 2, 3}
   slice = append(slice, 4, 5) // 自动扩容
   ```

3. **切片操作函数**：
   - **`append`**：
     ```go
     slice := []int{1, 2, 3}
     slice = append(slice, 4, 5) // 向切片追加元素
     ```
   - **`copy`**：
     ```go
     src := []int{1, 2, 3}
     dest := make([]int, 2)
     copy(dest, src) // 复制 src 到 dest
     ```

4. **切片的切割**：
   - **创建子切片**：
     ```go
     slice := []int{1, 2, 3, 4, 5}
     subSlice := slice[1:4] // 从索引 1 到 3（不包括 4）
     ```

### 切片的性能

下标读写是 O(1)：指针加下标一次算出地址。`append` 在容量够时也是 O(1)；容量不够时要按双倍增长重新分配并拷贝已有元素，单次 O(n)，连续 n 次 `append` 摊还下来仍是 O(1)。在头部插入或删除是 O(n)，后面所有元素都要搬一位。

切片共享底层数组，对其中一个切片的赋值可能改到另一个切片的数据，出问题时往往查不到源头。要隔离就用 `copy` 复制一份，或用 `s[i:j:j]` 限制容量。

### 切片的示例代码

以下是几个常见的切片操作示例：

```go
package main

import (
    "fmt"
)

func main() {
    // 创建切片
    slice := []int{1, 2, 3, 4, 5}
    fmt.Println("Original Slice:", slice)

    // 切割切片
    subSlice := slice[1:4]
    fmt.Println("Sub Slice:", subSlice)

    // 修改切片
    slice[2] = 10
    fmt.Println("Modified Original Slice:", slice)
    fmt.Println("Sub Slice After Modification:", subSlice)

    // 追加元素
    slice = append(slice, 6, 7)
    fmt.Println("Slice After Append:", slice)

    // 使用 make 创建切片
    newSlice := make([]int, 3, 5)
    fmt.Println("New Slice:", newSlice)

    // 复制切片
    src := []int{1, 2, 3}
    dest := make([]int, len(src))
    copy(dest, src)
    fmt.Println("Destination Slice After Copy:", dest)
}
```

### 总结

切片用指针、长度、容量三个字段描述一段底层数组，`append` 在容量不足时按双倍增长扩容，扩容可能重新分配内存。多个切片可能共享同一个底层数组，一处修改会波及其他切片，这是切片出错最常见的来源。