# 队列

队列（Queue）是一种先进先出（FIFO）的线性数据结构：元素从队尾入队（enqueue），从队首出队（dequeue）。用带尾指针的单向链表实现，两个操作都可以做到 $O(1)$。

### 核心操作

1. **Enqueue**: 在队尾追加元素。
2. **Dequeue**: 移除并返回队首元素。
3. **Front**: 查看队首元素但不移除。

### 实现要点

- 同时维护 `head` 和 `tail` 指针：出队走 `head`，入队走 `tail`。
- 只用头指针时，入队必须遍历到尾部，退化为 $O(n)$。
- 队列为空时 `head == nil`，入队后要让 `head` 和 `tail` 同时指向新节点。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// qNode 链表节点
type qNode struct {
	val  int
	next *qNode
}

// LinkedQueue 基于单向链表的队列
type LinkedQueue struct {
	head *qNode
	tail *qNode
	n    int
}

// Enqueue 入队
func (q *LinkedQueue) Enqueue(v int) {
	node := &qNode{val: v}
	if q.tail == nil {
		q.head = node
		q.tail = node
	} else {
		q.tail.next = node
		q.tail = node
	}
	q.n++
}

// Dequeue 出队
func (q *LinkedQueue) Dequeue() (int, bool) {
	if q.head == nil {
		return 0, false
	}
	v := q.head.val
	q.head = q.head.next
	if q.head == nil {
		q.tail = nil
	}
	q.n--
	return v, true
}

// Len 队列长度
func (q *LinkedQueue) Len() int { return q.n }

func main() {
	q := &LinkedQueue{}
	for _, v := range []int{1, 2, 3} {
		q.Enqueue(v)
	}
	fmt.Println("len:", q.Len())

	v, _ := q.Dequeue()
	fmt.Println("dequeue:", v)
	q.Enqueue(4)

	for {
		v, ok := q.Dequeue()
		if !ok {
			break
		}
		fmt.Println("dequeue:", v)
	}
	_, ok := q.Dequeue()
	fmt.Println("empty dequeue ok:", ok)
}
```

运行输出：

```text
len: 3
dequeue: 1
dequeue: 2
dequeue: 3
dequeue: 4
empty dequeue ok: false
```

### 复杂度分析

- **Enqueue / Dequeue**: $O(1)$。
- **空间**: $O(n)$。

### 应用场景

- 任务调度、消息缓冲、广度优先搜索（BFS）。
- 生产者-消费者模型中的等待队列。

### 总结

链表队列通过头尾双指针把入队和出队都做到 $O(1)$，且没有环形数组那样需要处理"假溢出"的问题；如果需要固定容量，可以改用环形缓冲区实现。
