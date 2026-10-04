# 双端队列
双端队列（Deque，Double-Ended Queue）是一种允许在两端进行插入和删除操作的数据结构，可以用数组实现。

### 双端队列的基本操作

插入、删除、访问三类操作各有前端和后端两个版本：插入、删除改变队列内容，访问只读取两端的元素。

### 数组实现的双端队列

数组实现要维护两个下标，分别指向队列的前端和后端：结构体里放一个定长数组、这两个下标和一个元素计数；插入和删除时按方向移动对应下标；队满或队空时做特殊处理，避免数组越界。

### 示例代码

下面是一个容量固定的 Go 实现：

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

`Deque` 用切片 `data` 做存储，`front` 和 `back` 是两端的下标，`size` 记录当前元素数量，并用来区分「队空」和「队满」。下标移动都写成 `+ len(dq.data)` 再取模，绕过数组边界时不会越界。

`AddFront`/`AddBack` 在两端插入，`RemoveFront`/`RemoveBack` 在两端删除并返回元素值，`Front`/`Back` 只读。队满时插入、队空时删除和访问都会 panic，调用前可以先用 `IsFull`/`IsEmpty` 判断。

### 复杂度

两端的插入、删除和访问都是 O(1)：只做下标加减再取模，不搬动元素。按值查找是 O(n)，得从一端依次扫到另一端。容量在构造时定死，操作过程中不分配内存。

### 总结

容量在创建时固定，之后不会扩容；两端插入、删除、访问都是常数次的下标运算。