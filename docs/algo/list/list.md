# 链表

链表（Linked List）是一种通过指针把零散内存块串联起来的线性数据结构。每个节点存放数据和指向后继（可能还有前驱）的指针，插入、删除只需修改指针，不需要移动元素。

### 链表的分类

1. **单向链表**: 每个节点只有一个 `next` 指针，只能从头向尾遍历。
2. **双向链表**: 节点同时持有 `prev` 和 `next`，可以双向遍历。
3. **循环链表**: 尾节点的 `next` 指回头节点，形成一个环。

### 链表与数组对比

| 操作 | 数组 | 链表 |
| ---- | ---- | ---- |
| 随机访问 | $O(1)$ | $O(n)$ |
| 头部插入/删除 | $O(n)$ | $O(1)$ |
| 已知节点后插入/删除 | $O(n)$ | $O(1)$ |
| 内存 | 连续 | 离散，指针额外开销 |

### 代码示例（Go语言实现）

下面用 Go 标准库 `container/list` 演示双向链表的常见操作，并展示手写单向链表的反转：

```go
package main

import (
	"container/list"
	"fmt"
)

// ListNode 单向链表节点
type ListNode struct {
	Val  int
	Next *ListNode
}

// reverse 反转单向链表
func reverse(head *ListNode) *ListNode {
	var prev *ListNode
	for head != nil {
		head.Next, prev, head = prev, head, head.Next
	}
	return prev
}

func printChain(head *ListNode) {
	for p := head; p != nil; p = p.Next {
		fmt.Printf("%d -> ", p.Val)
	}
	fmt.Println("nil")
}

func main() {
	// 标准库双向链表
	l := list.New()
	e2 := l.PushBack(2)      // [2]
	l.PushFront(1)           // [1 2]
	l.InsertBefore(0, e2)    // [1 0 2]
	l.PushBack(3)            // [1 0 2 3]
	l.Remove(l.Front().Next()) // 删除 0 -> [1 2 3]

	for e := l.Front(); e != nil; e = e.Next() {
		fmt.Printf("%d ", e.Value)
	}
	fmt.Println()

	// 手写单向链表并反转
	head := &ListNode{1, &ListNode{2, &ListNode{3, nil}}}
	printChain(head)
	printChain(reverse(head))
}
```

运行输出：

```text
1 2 3 
1 -> 2 -> 3 -> nil
3 -> 2 -> 1 -> nil
```

### 复杂度分析

- **查找**: $O(n)$，需要沿指针逐个访问。
- **头部插入/删除**: $O(1)$。
- **指定位置后插入/删除**: $O(1)$（已持有该节点指针时）。

### 总结

链表用指针换取了灵活的插入删除能力，代价是失去了随机访问。掌握单向链表的反转、快慢指针等基础套路，是学习跳表、LRU 缓存等复合结构的前提。
