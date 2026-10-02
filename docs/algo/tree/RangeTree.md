# 区间树

区间树（Interval Tree）是为"区间集合"设计的搜索结构，支持插入区间、查询与给定区间**重叠（相交）** 的区间等操作。本篇采用"按左端点建立二叉搜索树 + 每个节点附加子树最大右端点"的经典增强方案：`MaxHigh` 提供了强大的剪枝能力，使重叠查询在 $O(\log n)$ 期望时间内完成。

### 结构定义

1. **BST 键**: 区间的左端点 `Low`，所有区间按 `Low` 有序。
2. **增强信息 `MaxHigh`**: 以该节点为根的子树中所有区间的最大右端点。
3. **查询剪枝**: 若左子树的 `MaxHigh < 查询区间左端`，则左子树所有区间都在查询区间左侧，不可能重叠——直接跳过。

### 算法步骤

1. **插入**: 按 `Low` 走 BST 路径挂上新节点，回溯时用左右孩子与自身更新 `MaxHigh`。
2. **重叠查询 `FindOverlap(l, h)`**:
   - 若左子树存在且 `left.MaxHigh >= l`，深入左子树继续找；
   - 否则检查当前区间：与 `[l, h]` 重叠则返回；若当前 `Low <= h` 但不重叠（区间整体在查询区间左侧），深入右子树；
   - 若当前 `Low > h`，右子树的 `Low` 更大，直接返回未找到。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// Interval 闭区间 [Low, High]
type Interval struct {
	Low, High int
}

// ITreeNode 区间树节点
type ITreeNode struct {
	Iv      Interval
	Left    *ITreeNode
	Right   *ITreeNode
	MaxHigh int // 子树中最大的 High
}

// Insert 插入区间，返回新的子树根
func Insert(n *ITreeNode, iv Interval) *ITreeNode {
	if n == nil {
		return &ITreeNode{Iv: iv, MaxHigh: iv.High}
	}
	if iv.Low < n.Iv.Low {
		n.Left = Insert(n.Left, iv)
	} else {
		n.Right = Insert(n.Right, iv)
	}
	// 上浮 MaxHigh
	n.MaxHigh = n.Iv.High
	if n.Left != nil && n.Left.MaxHigh > n.MaxHigh {
		n.MaxHigh = n.Left.MaxHigh
	}
	if n.Right != nil && n.Right.MaxHigh > n.MaxHigh {
		n.MaxHigh = n.Right.MaxHigh
	}
	return n
}

// FindOverlap 查找与 [l, h] 重叠的任意一个区间
func FindOverlap(n *ITreeNode, l, h int) (Interval, bool) {
	for n != nil {
		if n.Left != nil && n.Left.MaxHigh >= l {
			// 左子树可能有重叠，深入左子树
			n = n.Left
		} else if n.Iv.Low <= h {
			if n.Iv.High >= l {
				return n.Iv, true // 当前区间重叠
			}
			// 当前区间整体在查询区间左侧，重叠只可能在右子树
			n = n.Right
		} else {
			return Interval{}, false // 右子树所有 Low 更大，不可能重叠
		}
	}
	return Interval{}, false
}

// overlapOf 判断两个区间是否重叠（辅助：用于验证）
func overlapOf(a, b Interval) bool {
	return a.Low <= b.High && b.Low <= a.High
}

func main() {
	var root *ITreeNode
	for _, iv := range []Interval{
		{15, 20}, {10, 30}, {17, 19}, {5, 20}, {12, 14},
	} {
		root = Insert(root, iv)
	}

	query := Interval{18, 18}
	got, ok := FindOverlap(root, query.Low, query.High)
	fmt.Println("查询与 [18,18] 重叠的区间:", ok, got)

	query2 := Interval{21, 24}
	got2, ok2 := FindOverlap(root, query2.Low, query2.High)
	fmt.Println("查询与 [21,24] 重叠的区间:", ok2, got2)

	query3 := Interval{31, 40}
	_, ok3 := FindOverlap(root, query3.Low, query3.High)
	fmt.Println("查询与 [31,40] 重叠的区间:", ok3) // 应为 false
}
```

运行输出：

```text
查询与 [18,18] 重叠的区间: true {5 20}
查询与 [21,24] 重叠的区间: true {10 30}
查询与 [31,40] 重叠的区间: false
```

### 复杂度分析

- **插入**: $O(\log n)$（按左端点的 BST 深度）。
- **重叠查询**: $O(\log n)$ 期望（最坏 $O(n)$，退化成链时）。
- **空间**: $O(n)$，每节点额外一个 `MaxHigh` 字段。

### 应用场景

- 任务调度中的"时间窗口是否被占用"。
- 区间着色、重叠计数、基因组区间比对等。

### 总结

区间树没有发明新的树形，而是在 BST 之上附加了"子树最大右端点"这一条聚合信息——正是它让查询可以整枝剪掉不可能重叠的子树。它示范了增强 BST（augmented BST）的通用套路：为查询目标选择一条可上浮的路径信息。
