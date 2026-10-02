# 斐波那契堆

斐波那契堆（Fibonacci Heap）是一种可合并堆：它把"插入、取最小"做到 $O(1)$ 均摊，把"减小关键字、删除最小"分别做到 $O(1)$ 与 $O(\log n)$ 均摊。它的结构很松散——根表与各树的孩子链都是双向循环链表，只在删除最小节点时才做一次 `consolidate` 整理，把度数相同的树两两合并。

### 结构定义

1. **节点**: 关键字 `key`、度数 `degree`（孩子个数）、`mark` 标记、双向循环链表指针 `left/right`、`child` 与 `parent`。
2. **堆**: 根表（所有树根构成的双向循环链表）+ 指向最小节点的 `min` 指针 + 节点总数。
3. **最小性质**: `min` 永远指向根表中关键字最小的节点。

### 算法步骤

1. **插入**: 新节点拼进根表，必要时更新 `min`。均摊 $O(1)$。
2. **删除最小**: 摘下 `min`，把它的孩子全部提升进根表，然后 `consolidate`：按度数分桶，度数相同的两棵树关键字小的做根，直到根表中度数互不相同。
3. **减小关键字**: 改小后若破坏堆序，把该节点"剪切"回根表；父节点若已有被剪切走的孩子（`mark`），则继续级联剪切。均摊 $O(1)$。
4. `mark` 的含义：该节点自成为某节点孩子后，已失去过一个孩子。级联剪切正是用它保证树不会退化得太深，从而支撑均摊界。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// fibNode 斐波那契堆节点
type fibNode struct {
	key           int
	degree        int
	mark          bool
	parent, child *fibNode
	left, right   *fibNode
}

// FibHeap 斐波那契堆：min 指向根表中关键字最小的节点
type FibHeap struct {
	min *fibNode
	n   int
}

// Insert 插入新节点，返回该节点（便于后续 DecreaseKey）
func (h *FibHeap) Insert(key int) *fibNode {
	x := &fibNode{key: key}
	if h.min == nil {
		x.left, x.right = x, x
		h.min = x
	} else {
		x.left = h.min
		x.right = h.min.right
		h.min.right.left = x
		h.min.right = x
		if x.key < h.min.key {
			h.min = x
		}
	}
	h.n++
	return x
}

// Minimum 返回最小关键字
func (h *FibHeap) Minimum() int { return h.min.key }

// link 把 y 从根表摘下，变成 x 的孩子
func (h *FibHeap) link(y, x *fibNode) {
	y.left.right = y.right
	y.right.left = y.left
	y.parent = x
	if x.child == nil {
		x.child = y
		y.left, y.right = y, y
	} else {
		y.left = x.child
		y.right = x.child.right
		x.child.right.left = y
		x.child.right = y
	}
	x.degree++
	y.mark = false
}

// consolidate 合并根表中度数相同的树
func (h *FibHeap) consolidate() {
	const maxD = 64
	a := make([]*fibNode, maxD)

	// 先把当前根表快照下来，再逐个处理
	var roots []*fibNode
	x := h.min
	for {
		roots = append(roots, x)
		x = x.right
		if x == h.min {
			break
		}
	}
	for _, w := range roots {
		x := w
		d := x.degree
		for a[d] != nil {
			y := a[d]
			if x.key > y.key {
				x, y = y, x // 关键字小的做根
			}
			h.link(y, x)
			a[d] = nil
			d++
		}
		a[d] = x
	}

	// 用幸存的树根重建根表，并顺便找最小节点
	h.min = nil
	for _, w := range a {
		if w == nil {
			continue
		}
		w.left, w.right = w, w
		if h.min == nil {
			h.min = w
		} else {
			w.left = h.min
			w.right = h.min.right
			h.min.right.left = w
			h.min.right = w
			if w.key < h.min.key {
				h.min = w
			}
		}
	}
}

// ExtractMin 摘除最小节点，返回其关键字
func (h *FibHeap) ExtractMin() int {
	z := h.min
	// 把 z 的孩子全部提升进根表
	if z.child != nil {
		var cs []*fibNode
		c := z.child
		for {
			cs = append(cs, c)
			c = c.right
			if c == z.child {
				break
			}
		}
		for _, c := range cs {
			c.parent = nil
			c.mark = false
			c.left = h.min
			c.right = h.min.right
			h.min.right.left = c
			h.min.right = c
		}
		z.child = nil
	}
	// 从根表移除 z
	z.left.right = z.right
	z.right.left = z.left
	if z == z.right {
		h.min = nil
	} else {
		h.min = z.right
		h.consolidate()
	}
	h.n--
	return z.key
}

// cut 把 x 从父节点 y 的孩子表中剪切回根表
func (h *FibHeap) cut(x, y *fibNode) {
	if x.right == x {
		y.child = nil
	} else {
		x.left.right = x.right
		x.right.left = x.left
		if y.child == x {
			y.child = x.right
		}
	}
	y.degree--
	x.parent = nil
	x.mark = false
	x.left = h.min
	x.right = h.min.right
	h.min.right.left = x
	h.min.right = x
}

// cascadingCut 级联剪切：沿父链向上处理 mark 标记
func (h *FibHeap) cascadingCut(y *fibNode) {
	z := y.parent
	if z != nil {
		if !y.mark {
			y.mark = true
		} else {
			h.cut(y, z)
			h.cascadingCut(z)
		}
	}
}

// DecreaseKey 把 x 的关键字降到 k（要求 k <= x.key）
func (h *FibHeap) DecreaseKey(x *fibNode, k int) {
	x.key = k
	y := x.parent
	if y != nil && x.key < y.key {
		h.cut(x, y)
		h.cascadingCut(y)
	}
	if x.key < h.min.key {
		h.min = x
	}
}

func (h *FibHeap) Len() int { return h.n }

func main() {
	h := &FibHeap{}
	nodes := map[int]*fibNode{}
	for _, k := range []int{7, 3, 9, 1, 5, 8} {
		nodes[k] = h.Insert(k)
	}
	fmt.Println("最小值:", h.Minimum())
	h.DecreaseKey(nodes[9], 0)
	fmt.Println("把 9 降到 0 后最小值:", h.Minimum())

	fmt.Print("依次弹出:")
	for h.Len() > 0 {
		fmt.Print(" ", h.ExtractMin())
	}
	fmt.Println()
}
```

运行输出：

```text
最小值: 1
把 9 降到 0 后最小值: 0
依次弹出: 0 1 3 5 7 8
```

### 复杂度分析

| 操作 | 均摊复杂度 |
| --- | --- |
| Insert / Minimum | $O(1)$ |
| ExtractMin | $O(\log n)$ |
| DecreaseKey | $O(1)$ |
| 合并两个堆 | $O(1)$ |

- **空间**: $O(n)$。

### 应用场景

- Dijkstra 与 Prim 算法的理论最优实现：$O(E + V \log V)$，相比二叉堆少了 $\log V$ 因子乘在边数上。
- 需要频繁合并堆、减小关键字的图算法与调度器。

### 总结

斐波那契堆用"平时偷懒、删除时统一整理"的策略换取均摊复杂度：插入与减键只做指针拼接，把结构修复的成本全部推迟到 ExtractMin 一次结清。实践中常数较大，二叉堆往往更快，但处理稠密图最短路等场景时它是理论下界的不二之选。实现时最容易出错的是双向循环链表的拼接顺序与 `mark` 标记的维护。
