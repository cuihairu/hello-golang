# 队列

队列（Queue）是先进先出（FIFO）的线性数据结构：只允许在队尾入队（enqueue）、在队首出队（dequeue）。本篇用切片和环形数组两种方式实现队列，并演示它在广度优先搜索中的典型用法。

### 核心操作

1. **Enqueue**: 队尾加入元素。
2. **Dequeue**: 移除并返回队首元素。
3. **Peek**: 查看队首元素。

### 实现方式

1. **切片队列**: `enqueue` 用 `append`，`dequeue` 取 `q[0]` 后 `q = q[1:]`。简单直接，但 `q[1:]` 只移动切片头指针，底层数组不会被复用。
2. **环形切片队列**: 用 `head` 下标加 `count` 计数配合取模运算复用固定数组，内存占用恒定。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// IntQueue 基于环形切片的队列
type IntQueue struct {
	data  []int
	head  int
	count int
}

// NewIntQueue 创建容量为 n 的队列，满了会自动扩容
func NewIntQueue(n int) *IntQueue {
	return &IntQueue{data: make([]int, n)}
}

// Enqueue 入队
func (q *IntQueue) Enqueue(v int) {
	if q.count == len(q.data) { // 满则扩容
		grown := make([]int, len(q.data)*2)
		for i := 0; i < q.count; i++ {
			grown[i] = q.data[(q.head+i)%len(q.data)]
		}
		q.data = grown
		q.head = 0
	}
	q.data[(q.head+q.count)%len(q.data)] = v
	q.count++
}

// Dequeue 出队
func (q *IntQueue) Dequeue() (int, bool) {
	if q.count == 0 {
		return 0, false
	}
	v := q.data[q.head]
	q.head = (q.head + 1) % len(q.data)
	q.count--
	return v, true
}

// Len 队列长度
func (q *IntQueue) Len() int { return q.count }

func main() {
	q := NewIntQueue(2)
	for i := 1; i <= 5; i++ { // 故意超过初始容量，触发扩容
		q.Enqueue(i * 10)
	}
	fmt.Println("len:", q.Len())

	q.Dequeue() // 弹出 10
	v, _ := q.Dequeue()
	fmt.Println("second:", v)

	for {
		v, ok := q.Dequeue()
		if !ok {
			break
		}
		fmt.Println("dequeue:", v)
	}
}
```

运行输出：

```text
len: 5
second: 20
dequeue: 30
dequeue: 40
dequeue: 50
```

### 复杂度分析

- **Enqueue / Dequeue**: 均摊 $O(1)$。
- **空间**: 环形实现为 $O(\text{容量})$，切片实现可能与底层数组等长。

### 应用场景

- 广度优先搜索（BFS）、层序遍历。
- 任务队列、消息缓冲、打印池。

### 总结

队列的关键是"两端操作、首出尾进"。环形数组实现以取模换来了固定内存下的 $O(1)$ 出入队，是标准库 `container/ring`、channel 内部缓冲等机制的共同思想。
