# 满二叉树

满二叉树（Full/Perfect Binary Tree）是"每一层都放满"的二叉树：高度为 $h$ 的满二叉树恰好有 $2^h - 1$ 个节点，第 $i$ 层（从 0 开始）恰好有 $2^i$ 个节点。英文语境中的 full binary tree 有时指"每个节点要么是叶子要么有两个孩子"（严格二叉树），本篇按国内教材常用的"每层填满"含义展开，并在代码中同时验证这两个性质。

### 性质

1. **节点数**: 高度 $h$ 的满二叉树共 $2^h - 1$ 个节点。
2. **叶子数**: 第 $h-1$ 层有 $2^{h-1}$ 个叶子，占全部节点的一半。
3. **编号关系**: 按层序编号 $1..2^h-1$，编号 $i$ 的父节点是 $\lfloor i/2 \rfloor$，孩子是 $2i$ 与 $2i+1$。

### 算法步骤（构建与验证）

1. **构建**: 按层序数组递归构建，下标 `i` 的孩子为 `2i+1、2i+2`，数组用满即得满二叉树。
2. **逐层统计**: BFS 记录每层节点数，验证第 `i` 层有 $2^i$ 个节点。
3. **验证总节点数**: `count == (1 << height) - 1`。

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

// build 按层序数组构建二叉树（数组被完全使用时得到满二叉树）
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

// levelSizes 返回每一层的节点数
func levelSizes(root *BNode) []int {
	var sizes []int
	queue := []*BNode{root}
	for len(queue) > 0 {
		n := len(queue)
		sizes = append(sizes, n)
		var next []*BNode
		for _, node := range queue {
			if node.Left != nil {
				next = append(next, node.Left)
			}
			if node.Right != nil {
				next = append(next, node.Right)
			}
		}
		queue = next
	}
	return sizes
}

// count 统计节点总数
func count(root *BNode) int {
	if root == nil {
		return 0
	}
	return 1 + count(root.Left) + count(root.Right)
}

func main() {
	// 高度为 3 的满二叉树，共 7 个节点
	root := build([]int{1, 2, 3, 4, 5, 6, 7}, 0)

	sizes := levelSizes(root)
	fmt.Println("每层节点数:", sizes) // [1 2 4]

	height := len(sizes)
	fmt.Println("高度:", height)
	fmt.Println("节点总数:", count(root), "理论值:", (1<<height)-1)

	// 对照：每层第 i 层应有 2^i 个节点
	ok := true
	for i, s := range sizes {
		if s != 1<<i {
			ok = false
		}
	}
	fmt.Println("是满二叉树:", ok)
}
```

运行输出：

```text
每层节点数: [1 2 4]
高度: 3
节点总数: 7 理论值: 7
是满二叉树: true
```

### 复杂度分析

- **构建/遍历/统计**: $O(n)$，$n = 2^h - 1$ 为节点总数。
- **空间**: 递归深度 $O(h) = O(\log n)$。

### 总结

满二叉树是形态最"整齐"的二叉树：节点数、层数、孩子位置之间都是确定的指数关系。它是分析堆、线段树等结构空间上限时使用的基准形态，也是完全二叉树、严格二叉树等概念的参照物。
