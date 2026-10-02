# 树

树（Tree）是由 $n \geq 0$ 个节点组成的分层非线性结构：有一个根节点，其余节点被分成若干互不相交的子树。文件系统、组织架构、DOM 都是典型的树形结构。

### 基本术语

1. **根节点（Root）**: 没有父节点的节点。
2. **叶子节点（Leaf）**: 没有孩子的节点。
3. **度（Degree）**: 节点拥有的孩子数量。
4. **深度（Depth）**: 从根到该节点路径上的边数。
5. **高度（Height）**: 树中节点深度的最大值。

### 常见操作

1. **深度优先遍历（DFS）**: 先访问根节点，再依次递归访问每棵子树（先根序）。
2. **广度优先遍历（BFS）**: 借助队列按层访问。
3. **求高度**: 孩子高度的最大值加 1。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"strings"
)

// TreeNode 树节点，Children 保存所有孩子
type TreeNode struct {
	Val      string
	Children []*TreeNode
}

// AddChild 添加孩子节点
func (n *TreeNode) AddChild(child *TreeNode) {
	n.Children = append(n.Children, child)
}

// DepthFirst 深度优先遍历（先根序）
func DepthFirst(node *TreeNode, depth int) {
	if node == nil {
		return
	}
	fmt.Printf("%s- %s\n", strings.Repeat("  ", depth), node.Val)
	for _, c := range node.Children {
		DepthFirst(c, depth+1)
	}
}

// BreadthFirst 广度优先遍历（按层）
func BreadthFirst(root *TreeNode) {
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		fmt.Printf("%s ", node.Val)
		queue = append(queue, node.Children...)
	}
	fmt.Println()
}

// Height 计算树的高度（以节点数计）
func Height(node *TreeNode) int {
	if node == nil {
		return 0
	}
	best := 0
	for _, c := range node.Children {
		if h := Height(c); h > best {
			best = h
		}
	}
	return best + 1
}

func main() {
	root := &TreeNode{Val: "公司"}
	rd := &TreeNode{Val: "研发部"}
	mkt := &TreeNode{Val: "市场部"}
	root.AddChild(rd)
	root.AddChild(mkt)
	rd.AddChild(&TreeNode{Val: "前端组"})
	rd.AddChild(&TreeNode{Val: "后端组"})

	DepthFirst(root, 0)
	BreadthFirst(root)
	fmt.Println("height:", Height(root))
}
```

运行输出：

```text
- 公司
  - 研发部
    - 前端组
    - 后端组
  - 市场部
公司 研发部 市场部 前端组 后端组 
height: 3
```

### 复杂度分析

- **遍历**: $O(n)$，每个节点访问一次；BFS 额外需要 $O(w)$ 的队列空间（$w$ 为最大宽度）。
- **求高度**: $O(n)$。
- **存储**: 每个节点保存孩子指针切片，总空间 $O(n)$。

### 总结

树把"一对多"的层级关系表达为孩子指针的集合；用递归描述树上的操作通常最自然。二叉树、堆、字典树等都是它的特例，后续章节将逐一展开。
