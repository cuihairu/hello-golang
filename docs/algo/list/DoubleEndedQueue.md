# 双端队列

双端队列（Double Ended Queue，Deque）允许在队列的两端都可以进行插入和删除操作，同时兼具栈和队列的能力。

### 结构特点

1. **两端操作**: 支持 `PushFront`、`PushBack`、`PopFront`、`PopBack` 四个核心操作。
2. **双向链表实现**: 用带 `prev/next` 指针的节点实现，两端操作都是 $O(1)$。
3. **切片实现**: Go 中也可以用 `container/list` 或切片模拟，切片版 `PushFront` 为 $O(n)$。

### 常见操作

1. **PushFront / PushBack**: 在头部/尾部插入元素。
2. **PopFront / PopBack**: 移除并返回头部/尾部元素。
3. **Peek**: 只读取队首或队尾元素而不删除。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// dequeNode 双向链表节点
type dequeNode struct {
	val  int
	prev *dequeNode
	next *dequeNode
}

// Deque 基于双向链表的双端队列
type Deque struct {
	front *dequeNode
	back  *dequeNode
	size  int
}

// PushFront 头部插入
func (d *Deque) PushFront(v int) {
	n := &dequeNode{val: v, next: d.front}
	if d.front != nil {
		d.front.prev = n
	} else {
		d.back = n
	}
	d.front = n
	d.size++
}

// PushBack 尾部插入
func (d *Deque) PushBack(v int) {
	n := &dequeNode{val: v, prev: d.back}
	if d.back != nil {
		d.back.next = n
	} else {
		d.front = n
	}
	d.back = n
	d.size++
}

// PopFront 头部弹出
func (d *Deque) PopFront() (int, bool) {
	if d.size == 0 {
		return 0, false
	}
	v := d.front.val
	d.front = d.front.next
	if d.front != nil {
		d.front.prev = nil
	} else {
		d.back = nil
	}
	d.size--
	return v, true
}

// PopBack 尾部弹出
func (d *Deque) PopBack() (int, bool) {
	if d.size == 0 {
		return 0, false
	}
	v := d.back.val
	d.back = d.back.prev
	if d.back != nil {
		d.back.next = nil
	} else {
		d.front = nil
	}
	d.size--
	return v, true
}

func main() {
	d := &Deque{}
	d.PushBack(1)
	d.PushBack(2)
	d.PushFront(0)
	d.PushFront(-1)

	// 队列内容: [-1 0 1 2]
	fmt.Println("PopBack:", mustPop(d.PopBack))   // 2
	fmt.Println("PopFront:", mustPop(d.PopFront)) // -1
	fmt.Println("PopBack:", mustPop(d.PopBack))   // 1
	fmt.Println("PopFront:", mustPop(d.PopFront)) // 0
	_, ok := d.PopFront()
	fmt.Println("empty:", ok == false)
}

func mustPop(f func() (int, bool)) int {
	v, ok := f()
	if !ok {
		panic("pop from empty deque")
	}
	return v
}
```

### 复杂度分析

- **两端插入/删除**: $O(1)$。
- **随机访问**: $O(n)$，需要沿指针移动。
- **空间**: $O(n)$。

### 应用场景

- 滑动窗口最大值（单调双端队列）。
- 实现"两端都可进出的任务队列"、撤销历史等。

### 总结

双端队列在链表基础上同时开放了两端的 $O(1)$ 插入删除，是栈与队列的统一体；配合"保持单调性"的用法还能高效解决滑动窗口类问题。
