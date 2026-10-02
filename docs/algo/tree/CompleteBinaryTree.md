# 完全二叉树

完全二叉树（Complete Binary Tree）是一棵"只允许最后一层缺右边"的二叉树：除最后一层外每层都填满，最后一层的节点必须从左到右连续排列。这一性质使它可以被紧凑地存进数组而不浪费空间——二叉堆正是建立在这个性质之上。

### 性质

1. **同高度的满二叉树最省空间的二叉树**: 不存在"空洞"节点。
2. **数组表示**: 按层序存入数组，下标 `i` 的左孩子为 `2i+1`、右孩子为 `2i+2`、父节点为 `(i-1)/2`，数组中不会出现空洞。
3. **高度**: $O(\log n)$，$n$ 个节点的完全二叉树高度为 $\lfloor \log_2 n \rfloor$。

### 算法步骤（判断完全二叉树）

1. 对树做层序遍历（BFS），`nil` 孩子也入队。
2. 一旦遇到 `nil`，标记 `seenNil = true`。
3. 若在 `seenNil` 之后又出现非空节点，说明左侧有空洞，不是完全二叉树。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// BNode 二叉树节点
type BNode struct {
	Val   int
	Left  *BNode
	Right *BNode
}

// isComplete 判断二叉树是否为完全二叉树
func isComplete(root *BNode) bool {
	if root == nil {
		return true
	}
	queue := []*BNode{root}
	seenNil := false
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if node == nil {
			seenNil = true
			continue
		}
		if seenNil {
			return false // 空洞之后又出现了节点
		}
		queue = append(queue, node.Left, node.Right)
	}
	return true
}

// build 按层序数组构建二叉树
func build(values []int, i int) *BNode {
	if i >= len(values) {
		return nil
	}
	return &BNode{
		Val:   values[i],
		Left:  build(values, 2*i+1),
		Right: build(values, 2*i+2),
	}
}

func main() {
	complete := build([]int{1, 2, 3, 4, 5, 6}, 0)
	fmt.Println("tree1 complete:", isComplete(complete))

	// 3 的左孩子为空但右孩子存在，破坏了"从左到右连续"
	notComplete := &BNode{
		Val:   1,
		Left:  &BNode{Val: 2},
		Right: &BNode{Val: 3, Right: &BNode{Val: 6}},
	}
	fmt.Println("tree2 complete:", isComplete(notComplete))
}
```

运行输出：

```text
tree1 complete: true
tree2 complete: false
```

### 复杂度分析

- **判断完全性**: $O(n)$ 时间，$O(n)$ 队列空间。
- **数组表示下的访问父子**: $O(1)$（纯下标计算）。

### 应用场景

- 二叉堆 / 优先队列的底层形态。
- 堆排序、线段树的数组式存储。

### 总结

完全二叉树的核心价值是"没有空洞"，因此能无损地映射为数组，父子关系只用下标运算即可表达。判断完全性的关键是发现"空节点之后不能再有非空节点"。
