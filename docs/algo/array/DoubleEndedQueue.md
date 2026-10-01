# 双端队列
双端队列（Deque，Double-Ended Queue）是一种允许在两端进行插入和删除操作的数据结构。双端队列可以用数组实现，提供了高效的双端操作。下面是如何使用数组实现双端队列的详细说明。

### 双端队列的基本操作

1. **插入操作**：
   - **前端插入**：在队列的前端插入一个新元素。
   - **后端插入**：在队列的后端插入一个新元素。

2. **删除操作**：
   - **前端删除**：从队列的前端移除一个元素。
   - **后端删除**：从队列的后端移除一个元素。

3. **访问操作**：
   - **前端访问**：访问队列的前端元素。
   - **后端访问**：访问队列的后端元素。

### 数组实现的双端队列

在数组实现的双端队列中，我们需要管理两个指针或索引，分别指向队列的前端和后端。以下是双端队列的实现步骤：

1. **定义结构体**：
   - 使用数组作为存储容器。
   - 使用两个索引分别标记前端和后端。

2. **实现插入和删除操作**：
   - 处理前端和后端的插入和删除操作，同时更新相应的索引。

3. **处理边界情况**：
   - 处理队列满或空的情况，避免数组越界。

### 示例代码

以下是用 Go 语言实现的双端队列的示例代码：

```go
package main

import (
    "fmt"
)

type Deque struct {
    data       []int
    front, back int
    size       int
}

func NewDeque(capacity int) *Deque {
    return &Deque{
        data:  make([]int, capacity),
        front: -1,
        back: 0,
        size:  0,
    }
}

func (dq *Deque) IsEmpty() bool {
    return dq.size == 0
}

func (dq *Deque) IsFull() bool {
    return dq.size == len(dq.data)
}

func (dq *Deque) AddFront(value int) {
    if dq.IsFull() {
        panic("Deque is full")
    }
    if dq.IsEmpty() {
        dq.front = 0
        dq.back = 0
    } else {
        dq.front = (dq.front - 1 + len(dq.data)) % len(dq.data)
    }
    dq.data[dq.front] = value
    dq.size++
}

func (dq *Deque) AddBack(value int) {
    if dq.IsFull() {
        panic("Deque is full")
    }
    if dq.IsEmpty() {
        dq.front = 0
        dq.back = 0
    } else {
        dq.back = (dq.back + 1) % len(dq.data)
    }
    dq.data[dq.back] = value
    dq.size++
}

func (dq *Deque) RemoveFront() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    value := dq.data[dq.front]
    dq.front = (dq.front + 1) % len(dq.data)
    dq.size--
    if dq.IsEmpty() {
        dq.front = -1
        dq.back = 0
    }
    return value
}

func (dq *Deque) RemoveBack() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    value := dq.data[dq.back]
    dq.back = (dq.back - 1 + len(dq.data)) % len(dq.data)
    dq.size--
    if dq.IsEmpty() {
        dq.front = -1
        dq.back = 0
    }
    return value
}

func (dq *Deque) Front() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    return dq.data[dq.front]
}

func (dq *Deque) Back() int {
    if dq.IsEmpty() {
        panic("Deque is empty")
    }
    return dq.data[dq.back]
}

func main() {
    deque := NewDeque(5)

    deque.AddBack(1)
    deque.AddBack(2)
    deque.AddFront(3)
    deque.AddFront(4)
    fmt.Println("Front:", deque.Front()) // Output: Front: 4
    fmt.Println("Back:", deque.Back())   // Output: Back: 2

    fmt.Println("Removed from front:", deque.RemoveFront()) // Output: Removed from front: 4
    fmt.Println("Removed from back:", deque.RemoveBack())   // Output: Removed from back: 2
}
```

### 代码解析

1. **结构体定义**：
   - `Deque` 结构体包括一个整数切片 `data` 作为存储容器，`front` 和 `back` 指示前端和后端的索引，`size` 记录当前元素数量。

2. **方法实现**：
   - `AddFront` 和 `AddBack` 方法分别用于在前端和后端添加元素。
   - `RemoveFront` 和 `RemoveBack` 方法分别用于从前端和后端移除元素。
   - `Front` 和 `Back` 方法分别用于访问前端和后端的元素。

3. **处理边界情况**：
   - 处理队列满（`IsFull`）和空（`IsEmpty`）的情况。

### 总结

使用数组实现的双端队列提供了高效的双端操作，同时通过适当的索引管理和边界条件处理，实现了一个灵活的队列数据结构。