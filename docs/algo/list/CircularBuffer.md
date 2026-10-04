# 环形缓冲区

环形缓冲区（Circular Buffer，也叫 Ring Buffer）把一段固定长度的数组首尾相连当成"环"来使用，配合读指针和元素个数实现 FIFO 队列，常用于生产者-消费者之间的数据传递。

### 结构定义

1. **data**: 固定长度的底层数组。
2. **head**: 下一个读取位置的下标。
3. **count**: 当前元素个数，用它区分"空"和"满"。
4. **写入位置**: `(head + count) % len(data)`，越过数组末尾后自动绕回开头。

### 算法步骤

1. **写入**: 若已满则失败；否则计算写入下标，存放元素，`count++`。
2. **读取**: 若为空则失败；否则取出 `head` 处元素，`head = (head+1) % len(data)`，`count--`。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// CircularBuffer 固定容量的环形缓冲区
type CircularBuffer struct {
	data  []int
	head  int // 下一个读取的位置
	count int // 当前元素个数
}

// NewCircularBuffer 创建指定容量的环形缓冲区
func NewCircularBuffer(capacity int) *CircularBuffer {
	return &CircularBuffer{data: make([]int, capacity)}
}

// Len 当前元素个数
func (c *CircularBuffer) Len() int { return c.count }

// Empty 是否为空
func (c *CircularBuffer) Empty() bool { return c.count == 0 }

// Full 是否已满
func (c *CircularBuffer) Full() bool { return c.count == len(c.data) }

// Write 写入一个元素，缓冲区已满时返回 false
func (c *CircularBuffer) Write(v int) bool {
	if c.Full() {
		return false
	}
	idx := (c.head + c.count) % len(c.data)
	c.data[idx] = v
	c.count++
	return true
}

// Read 读取一个元素
func (c *CircularBuffer) Read() (int, bool) {
	if c.Empty() {
		return 0, false
	}
	v := c.data[c.head]
	c.head = (c.head + 1) % len(c.data)
	c.count--
	return v, true
}

func main() {
	c := NewCircularBuffer(3)
	for _, v := range []int{1, 2, 3} {
		fmt.Println("write", v, ":", c.Write(v))
	}
	fmt.Println("full:", c.Full(), "write 4:", c.Write(4))

	v, _ := c.Read()
	fmt.Println("read:", v)
	fmt.Println("write 4:", c.Write(4)) // 复用空出来的位置

	for !c.Empty() {
		v, _ := c.Read()
		fmt.Println("read:", v)
	}
	fmt.Println("empty:", c.Empty())
}
```

运行输出：

```text
write 1 : true
write 2 : true
write 3 : true
full: true write 4: false
read: 1
write 4: true
read: 2
read: 3
read: 4
empty: true
```

### 复杂度分析

- **读/写**: $O(1)$，无内存移动、无扩容。
- **空间**: 固定为容量 $k$。

### 应用场景

- 音视频帧缓冲、网络收发包队列。
- 生产者-消费者模型中的无锁（单生产者单消费者）队列。

### 总结

环形缓冲区用固定内存实现稳定的 FIFO 队列，通过取模运算让指针在数组内"绕圈"，避免了普通数组队列删除头部元素后的搬移与"假溢出"问题。
