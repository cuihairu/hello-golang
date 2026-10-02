# 笛卡尔树

笛卡尔树（Cartesian Tree）是给定一个数组后唯一确定的二叉树：**中序遍历等于原数组顺序**，同时是**最大堆**（任一节点是其子树中的最大值）。它把"数组的区间最大值"编码成了树形结构——数组任意区间的最大值恰好对应这段区间对应子树的根，因此是 RMQ（区间最值查询）问题的预处理结构。

### 构造方法（单调栈，O(n)）

从左到右扫描数组，用一个"值递减"的单调栈维护右链（根到当前最右叶子的路径）：

1. 新建节点 `node`，弹出栈顶所有值小于 `node.Val` 的节点，记录最后一个被弹出的节点 `last`。
2. 令 `node.Left = last`（最后弹出的较大子树成为左子树）。
3. 若栈非空，栈顶节点（大于等于 `node.Val`）的右孩子设为 `node`。
4. `node` 入栈。扫描结束后栈底元素即根。

### 区间最值（RMQ）

- 记录每个元素的下标。区间 `[i, j]` 的最大值节点 = 下标 `i` 与 `j` 在笛卡尔树中的**最近公共祖先（LCA）**。
- 查找 LCA 沿下标走即可，每次 $O(h)$。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// CNode 笛卡尔树节点
type CNode struct {
	Idx   int // 在原数组中的下标
	Val   int
	Left  *CNode
	Right *CNode
}

// buildMaxCartesian 单调栈构建最大笛卡尔树，O(n)
func buildMaxCartesian(arr []int) *CNode {
	var stack []*CNode
	for i, v := range arr {
		node := &CNode{Idx: i, Val: v}
		var last *CNode
		for len(stack) > 0 && stack[len(stack)-1].Val < v {
			last = stack[len(stack)-1]
			stack = stack[:len(stack)-1]
		}
		node.Left = last
		if len(stack) > 0 {
			stack[len(stack)-1].Right = node
		}
		stack = append(stack, node)
	}
	if len(stack) == 0 {
		return nil
	}
	return stack[0]
}

// inOrder 中序遍历（应等于原数组）
func inOrder(n *CNode, out *[]int) {
	if n == nil {
		return
	}
	inOrder(n.Left, out)
	*out = append(*out, n.Val)
	inOrder(n.Right, out)
}

// isMaxHeap 校验最大堆性质
func isMaxHeap(n *CNode) bool {
	if n == nil {
		return true
	}
	if n.Left != nil && n.Left.Val > n.Val {
		return false
	}
	if n.Right != nil && n.Right.Val > n.Val {
		return false
	}
	return isMaxHeap(n.Left) && isMaxHeap(n.Right)
}

// lca 求下标 i、j 的最近公共祖先
func lca(root *CNode, i, j int) *CNode {
	if root == nil {
		return nil
	}
	if i < root.Idx && j < root.Idx {
		return lca(root.Left, i, j)
	}
	if i > root.Idx && j > root.Idx {
		return lca(root.Right, i, j)
	}
	return root
}

// rangeMax 区间 [i, j] 的最大值
func rangeMax(root *CNode, i, j int) int {
	return lca(root, i, j).Val
}

func main() {
	arr := []int{3, 1, 5, 2, 4}
	root := buildMaxCartesian(arr)

	var out []int
	inOrder(root, &out)
	fmt.Println("中序遍历 == 原数组:", out)
	fmt.Println("满足最大堆:", isMaxHeap(root))

	fmt.Println("rangeMax[0..1] =", rangeMax(root, 0, 1)) // max(3, 1)
	fmt.Println("rangeMax[1..3] =", rangeMax(root, 1, 3)) // max(1, 5, 2)
	fmt.Println("rangeMax[3..4] =", rangeMax(root, 3, 4)) // max(2, 4)
	fmt.Println("rangeMax[0..4] =", rangeMax(root, 0, 4)) // max(全数组)
}
```

运行输出：

```text
中序遍历 == 原数组: [3 1 5 2 4]
满足最大堆: true
rangeMax[0..1] = 3
rangeMax[1..3] = 5
rangeMax[3..4] = 4
rangeMax[0..4] = 5
```

### 复杂度分析

- **构建**: $O(n)$，每个元素进出栈一次。
- **RMQ（单次）**: $O(h)$，平均 $O(\log n)$，最坏 $O(n)$；配合跳表/LCA 预处理可到 $O(1)$ 查询。
- **空间**: $O(n)$。

### 总结

笛卡尔树用两个平凡约束（中序还原数组 + 最大堆）唯一确定了一棵树，从而把数组的区间最值转化为 LCA 查询。单调栈构造只有一趟扫描，是理解"数组结构与树结构互译"的经典范例。
