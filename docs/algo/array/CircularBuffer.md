# 环形缓冲区

环形缓冲区（也叫循环缓冲区）是一块固定大小的缓冲区，数据在里面循环存放，适合流数据处理、任务队列这类要反复复用同一块空间的场景。

### 环形缓冲区概述

它由一个数组和两个索引组成：一个记读位置，一个记写位置。写索引走到数组末尾就绕回开头，形成一个“环”。读写因此都不必搬动已有数据。

### 环形缓冲区的基本操作

1. **初始化**:
   - 创建一个固定大小的数组作为缓冲区，并初始化读写指针。
   
   ```go
   type RingBuffer struct {
       buffer []byte
       size   int
       head   int
       tail   int
       count  int
   }

   func NewRingBuffer(size int) *RingBuffer {
       return &RingBuffer{
           buffer: make([]byte, size),
           size:   size,
           head:   0,
           tail:   0,
           count:  0,
       }
   }
   ```

2. **写入数据**:
   - 将数据写入缓冲区。写指针会在数组末尾回绕到开头，缓冲区已满时只写入剩余空间能容纳的部分，并返回实际写入的字节数。
   
   ```go
   func (rb *RingBuffer) Write(data []byte) int {
       n := len(data)
       if n > rb.size {
           n = rb.size
       }

       // 计算可以写入的字节数
       if rb.count+len(data) > rb.size {
           n = rb.size - rb.count
       }

       // 写入数据
       for i := 0; i < n; i++ {
           rb.buffer[rb.tail] = data[i]
           rb.tail = (rb.tail + 1) % rb.size
           rb.count++
       }

       return n
   }
   ```

3. **读取数据**:
   - 从缓冲区读取数据。读指针会在数组末尾回绕到开头。

   ```go
   func (rb *RingBuffer) Read(p []byte) int {
       n := len(p)
       if n > rb.count {
           n = rb.count
       }

       // 读取数据
       for i := 0; i < n; i++ {
           p[i] = rb.buffer[rb.head]
           rb.head = (rb.head + 1) % rb.size
           rb.count--
       }

       return n
   }
   ```

4. **检查缓冲区状态**:
   - 检查缓冲区是否已满，是否为空等。

   ```go
   func (rb *RingBuffer) IsFull() bool {
       return rb.count == rb.size
   }

   func (rb *RingBuffer) IsEmpty() bool {
       return rb.count == 0
   }
   ```

### 应用场景

1. **流数据处理**:
   - 在流数据处理中，环形缓冲区用于处理连续的数据流，比如网络数据包、实时传感器数据等。

2. **任务队列**:
   - 在生产者-消费者模型中，环形缓冲区可以作为任务队列，用于存储待处理的任务。

3. **音视频处理**:
   - 在音视频数据流中，环形缓冲区用于缓存数据，确保数据的连续性和稳定性。

### 优点

缓冲区大小固定，全程没有动态分配，也就没有内存碎片。读写只改索引、不搬数据，时间复杂度是 O(1)，同一块空间转着圈重复用，拷贝次数比顺序队列少。

### 示例代码

```go
package main

import (
    "fmt"
)

type RingBuffer struct {
    buffer []byte
    size   int
    head   int
    tail   int
    count  int
}

func NewRingBuffer(size int) *RingBuffer {
    return &RingBuffer{
        buffer: make([]byte, size),
        size:   size,
        head:   0,
        tail:   0,
        count:  0,
    }
}

func (rb *RingBuffer) Write(data []byte) int {
    n := len(data)
    if n > rb.size {
        n = rb.size
    }

    if rb.count+len(data) > rb.size {
        n = rb.size - rb.count
    }

    for i := 0; i < n; i++ {
        rb.buffer[rb.tail] = data[i]
        rb.tail = (rb.tail + 1) % rb.size
        rb.count++
    }

    return n
}

func (rb *RingBuffer) Read(p []byte) int {
    n := len(p)
    if n > rb.count {
        n = rb.count
    }

    for i := 0; i < n; i++ {
        p[i] = rb.buffer[rb.head]
        rb.head = (rb.head + 1) % rb.size
        rb.count--
    }

    return n
}

func (rb *RingBuffer) IsFull() bool {
    return rb.count == rb.size
}

func (rb *RingBuffer) IsEmpty() bool {
    return rb.count == 0
}

func main() {
    rb := NewRingBuffer(5)
    rb.Write([]byte("hello"))
    fmt.Println(rb.IsFull()) // true

    buf := make([]byte, 5)
    rb.Read(buf)
    fmt.Println(string(buf)) // "hello"

    rb.Write([]byte("world"))
    fmt.Println(rb.IsEmpty()) // false
}
```

main 里先写入 5 字节把缓冲区填满，`IsFull` 返回 true；读出后再写入 `world`，`IsEmpty` 返回 false。