# 栈

栈（Stack）是一种后进先出（LIFO）的线性数据结构，只能在栈顶进行插入和删除。用链表实现栈时，把头部当作栈顶，入栈和出栈都是 $O(1)$。

### 核心操作

1. **Push**: 把元素压入栈顶。
2. **Pop**: 弹出栈顶元素。
3. **Peek**: 查看栈顶元素但不弹出。
4. **IsEmpty / Len**: 判空与求长度。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// stackNode 链表节点
type stackNode struct {
	val  int
	next *stackNode
}

// LinkedStack 基于单向链表的栈
type LinkedStack struct {
	top *stackNode
	n   int
}

// Push 入栈
func (s *LinkedStack) Push(v int) {
	s.top = &stackNode{val: v, next: s.top}
	s.n++
}

// Pop 出栈
func (s *LinkedStack) Pop() (int, bool) {
	if s.top == nil {
		return 0, false
	}
	v := s.top.val
	s.top = s.top.next
	s.n--
	return v, true
}

// Peek 查看栈顶
func (s *LinkedStack) Peek() (int, bool) {
	if s.top == nil {
		return 0, false
	}
	return s.top.val, true
}

// Len 栈中元素个数
func (s *LinkedStack) Len() int { return s.n }

func main() {
	s := &LinkedStack{}
	for _, v := range []int{1, 2, 3} {
		s.Push(v)
	}
	fmt.Println("len:", s.Len())

	if v, ok := s.Peek(); ok {
		fmt.Println("peek:", v)
	}
	for {
		v, ok := s.Pop()
		if !ok {
			break
		}
		fmt.Println("pop:", v)
	}
	_, ok := s.Pop()
	fmt.Println("empty pop ok:", ok)
}
```

运行输出：

```text
len: 3
peek: 3
pop: 3
pop: 2
pop: 1
empty pop ok: false
```

### 复杂度分析

- **Push / Pop / Peek**: $O(1)$。
- **空间**: $O(n)$，每个节点一个额外指针。

### 应用场景

- 函数调用栈、括号匹配、表达式求值。
- 深度优先搜索（DFS）、浏览器前进后退等。

### 总结

链表实现的栈不需要扩容，每次操作都只涉及栈顶指针的修改；与切片实现的栈相比，它牺牲了缓存局部性，换来了稳定的 $O(1)$ 性能。
