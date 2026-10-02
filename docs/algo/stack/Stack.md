# 栈

栈（Stack）是后进先出（LIFO）的线性数据结构：所有插入（push）和删除（pop）都发生在栈顶。本篇用 Go 切片实现一个通用栈，并用它解决经典的"括号匹配"问题。

### 核心操作

1. **Push**: 元素入栈，成为新的栈顶。
2. **Pop**: 弹出并返回栈顶元素。
3. **Peek**: 查看栈顶但不弹出。
4. **IsEmpty**: 判断栈是否为空。

### 算法步骤（括号匹配）

1. 从左到右扫描字符串：
   - 遇到左括号 `(`、`[`、`{` 就压栈。
   - 遇到右括号时，若栈为空或栈顶不是对应的左括号，则不匹配；否则弹出栈顶。
2. 扫描结束后，栈为空说明所有括号正确闭合。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// Stack 基于切片的 int 栈
type Stack struct {
	items []int
}

// Push 入栈
func (s *Stack) Push(v int) {
	s.items = append(s.items, v)
}

// Pop 出栈
func (s *Stack) Pop() (int, bool) {
	if len(s.items) == 0 {
		return 0, false
	}
	n := len(s.items) - 1
	v := s.items[n]
	s.items = s.items[:n]
	return v, true
}

// Peek 查看栈顶
func (s *Stack) Peek() (int, bool) {
	if len(s.items) == 0 {
		return 0, false
	}
	return s.items[len(s.items)-1], true
}

// IsEmpty 是否为空
func (s *Stack) IsEmpty() bool { return len(s.items) == 0 }

// isMatched 判断括号串是否匹配
func isMatched(s string) bool {
	pairs := map[byte]byte{')': '(', ']': '[', '}': '{'}
	stack := make([]byte, 0, len(s))
	for i := 0; i < len(s); i++ {
		c := s[i]
		switch c {
		case '(', '[', '{':
			stack = append(stack, c)
		case ')', ']', '}':
			if len(stack) == 0 || stack[len(stack)-1] != pairs[c] {
				return false
			}
			stack = stack[:len(stack)-1]
		}
	}
	return len(stack) == 0
}

func main() {
	s := &Stack{}
	s.Push(1)
	s.Push(2)
	s.Push(3)
	if v, ok := s.Peek(); ok {
		fmt.Println("peek:", v)
	}
	for !s.IsEmpty() {
		v, _ := s.Pop()
		fmt.Println("pop:", v)
	}

	fmt.Println("()[]{} ->", isMatched("()[]{}"))
	fmt.Println("([)] ->", isMatched("([)]"))
	fmt.Println("{[()]} ->", isMatched("{[()]}"))
}
```

运行输出：

```text
peek: 3
pop: 3
pop: 2
pop: 1
()[]{} -> true
([)] -> false
{[()]} -> true
```

### 复杂度分析

- **Push / Pop / Peek**: 均摊 $O(1)$（切片扩容摊销后）。
- **空间**: $O(n)$。

### 应用场景

- 函数调用栈、递归的显式化改写。
- 括号匹配、表达式求值、深度优先搜索（DFS）、撤销操作。

### 总结

栈的规则最简单，却是表达式求值、DFS、递归等机制的骨架。切片实现的栈代码量最少，配合 `len-1` 的栈顶下标即可完成全部操作。
