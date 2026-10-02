# 静态链表

静态链表（Static Linked List）用数组来模拟链表：节点之间的逻辑关系不用指针，而用数组下标（游标）表示。它兼有数组"连续内存、下标访问"和链表"插入删除不改序"的特点，常见于没有指针的语言或嵌入式场景。

### 结构定义

1. **节点**: `data` 数据域 + `next` 游标域（下一个节点的数组下标）。
2. **空闲链**: 未使用的数组位置串成一条"空闲链表"，插入时从头摘取，删除后归还。
3. **头游标 `head`**: 第一个有效节点的下标，`-1` 表示空表。

### 算法步骤

1. **初始化**: 把所有位置的 `next` 串成空闲链，`head = -1`。
2. **插入第 i 位**: 从空闲链取一个位置存放新元素，沿 `next` 找到第 `i-1` 个节点，修改游标接入。
3. **删除第 i 位**: 沿 `next` 找到第 `i-1` 个节点，跳过目标节点，并把释放的位置归还空闲链。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

const maxSize = 10

type staticNode struct {
	data int
	next int // 下一个节点的数组下标，-1 表示结尾
}

// StaticLinkedList 数组实现的静态链表
type StaticLinkedList struct {
	nodes [maxSize]staticNode
	head  int
	free  int // 空闲链表头
	size  int
}

// NewStaticLinkedList 初始化：所有位置串成空闲链
func NewStaticLinkedList() *StaticLinkedList {
	s := &StaticLinkedList{head: -1, free: 0}
	for i := 0; i < maxSize-1; i++ {
		s.nodes[i].next = i + 1
	}
	s.nodes[maxSize-1].next = -1
	return s
}

// alloc 从空闲链取一个位置
func (s *StaticLinkedList) alloc() int {
	idx := s.free
	s.free = s.nodes[idx].next
	return idx
}

// Insert 在第 i 个位置（从 0 开始）插入 v
func (s *StaticLinkedList) Insert(i, v int) bool {
	if s.size >= maxSize || i < 0 || i > s.size {
		return false
	}
	idx := s.alloc()
	s.nodes[idx].data = v
	if i == 0 {
		s.nodes[idx].next = s.head
		s.head = idx
	} else {
		p := s.head
		for k := 0; k < i-1; k++ {
			p = s.nodes[p].next
		}
		s.nodes[idx].next = s.nodes[p].next
		s.nodes[p].next = idx
	}
	s.size++
	return true
}

// Remove 删除第 i 个位置的元素
func (s *StaticLinkedList) Remove(i int) (int, bool) {
	if i < 0 || i >= s.size {
		return 0, false
	}
	var idx int
	if i == 0 {
		idx = s.head
		s.head = s.nodes[idx].next
	} else {
		p := s.head
		for k := 0; k < i-1; k++ {
			p = s.nodes[p].next
		}
		idx = s.nodes[p].next
		s.nodes[p].next = s.nodes[idx].next
	}
	// 位置归还空闲链
	s.nodes[idx].next = s.free
	s.free = idx
	s.size--
	return s.nodes[idx].data, true
}

// Print 按逻辑顺序打印
func (s *StaticLinkedList) Print() {
	for p := s.head; p != -1; p = s.nodes[p].next {
		fmt.Printf("%d ", s.nodes[p].data)
	}
	fmt.Println()
}

func main() {
	s := NewStaticLinkedList()
	s.Insert(0, 10)
	s.Insert(1, 30)
	s.Insert(1, 20) // [10 20 30]
	s.Print()

	v, ok := s.Remove(1)
	fmt.Println("removed:", v, ok)
	s.Print()
	fmt.Println("size:", s.size)
}
```

运行输出：

```text
10 20 30 
removed: 20 true
10 30 
size: 2
```

### 复杂度分析

- **按位插入/删除**: 定位 $O(n)$，修改游标 $O(1)$。
- **按位访问**: 仍需 $O(n)$ 沿游标走（不是 $O(1)$，这是它与普通数组的关键区别）。
- **空间**: 容量固定为 `maxSize`，无指针开销。

### 总结

静态链表把链表的"指针"翻译成"数组下标"，在不能使用指针的环境里实现了链式存取；代价是容量固定、访问仍是线性，现代 Go 开发中更多是理解链表本质的教学模型。
