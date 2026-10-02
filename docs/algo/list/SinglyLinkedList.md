# 单向链表

单向链表（Singly Linked List）是最简单的链表形式：每个节点包含数据和一个指向后继节点的 `next` 指针，只能从头节点开始沿 `next` 方向遍历。

### 结构定义

1. **节点**: `data` 数据域 + `next` 后继指针。
2. **头节点 `head`**: 链表入口，`head == nil` 表示空链表。
3. **尾节点**: `next == nil` 的节点。

### 常见操作

1. **头部插入**: 新节点指向原头节点，再更新头节点，$O(1)$。
2. **尾部插入**: 沿 `next` 走到尾节点后挂接，$O(n)$；维护尾指针可优化为 $O(1)$。
3. **查找**: 从头遍历比较，$O(n)$。
4. **删除**: 找到目标的前驱节点，令 `prev.next = target.next`，$O(n)$。
5. **反转**: 逐个把节点的 `next` 指向前驱，$O(n)$。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// Node 单向链表节点
type Node struct {
	Val  int
	Next *Node
}

// SinglyLinkedList 带头指针的单向链表
type SinglyLinkedList struct {
	head *Node
	size int
}

// PushFront 头部插入，O(1)
func (s *SinglyLinkedList) PushFront(v int) {
	s.head = &Node{Val: v, Next: s.head}
	s.size++
}

// PushBack 尾部插入，O(n)
func (s *SinglyLinkedList) PushBack(v int) {
	n := &Node{Val: v}
	if s.head == nil {
		s.head = n
	} else {
		p := s.head
		for p.Next != nil {
			p = p.Next
		}
		p.Next = n
	}
	s.size++
}

// Remove 删除第一个值为 v 的节点
func (s *SinglyLinkedList) Remove(v int) bool {
	if s.head == nil {
		return false
	}
	if s.head.Val == v {
		s.head = s.head.Next
		s.size--
		return true
	}
	p := s.head
	for p.Next != nil && p.Next.Val != v {
		p = p.Next
	}
	if p.Next == nil {
		return false
	}
	p.Next = p.Next.Next
	s.size--
	return true
}

// Contains 判断是否包含值 v
func (s *SinglyLinkedList) Contains(v int) bool {
	for p := s.head; p != nil; p = p.Next {
		if p.Val == v {
			return true
		}
	}
	return false
}

// Reverse 反转链表
func (s *SinglyLinkedList) Reverse() {
	var prev *Node
	cur := s.head
	for cur != nil {
		cur.Next, prev, cur = prev, cur, cur.Next
	}
	s.head = prev
}

// Print 打印链表
func (s *SinglyLinkedList) Print() {
	for p := s.head; p != nil; p = p.Next {
		fmt.Printf("%d -> ", p.Val)
	}
	fmt.Println("nil")
}

func main() {
	s := &SinglyLinkedList{}
	s.PushBack(1)
	s.PushBack(2)
	s.PushFront(0)
	s.Print() // 0 -> 1 -> 2 -> nil

	fmt.Println("contains 2:", s.Contains(2))
	s.Remove(1)
	s.Print() // 0 -> 2 -> nil

	s.Reverse()
	s.Print() // 2 -> 0 -> nil
}
```

### 复杂度分析

- **头部插入/删除**: $O(1)$。
- **尾部插入/按值删除/查找**: $O(n)$。
- **空间**: 每个节点多一个指针，$O(n)$。

### 总结

单向链表结构简单、头部操作高效，适合作为栈、哈希桶拉链等结构的底层实现；由于不支持回退，删除节点时需要先找到前驱，这是它与双向链表的主要差距。
