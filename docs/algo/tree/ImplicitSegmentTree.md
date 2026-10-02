# 隐式线段树

隐式线段树（Implicit Segment Tree）是普通线段树的"懒惰创建"版本：不预先开 $4n$ 的数组，而是**用到哪个节点才创建哪个节点**。当区间巨大（例如 $[0, 10^9)$）而实际只操作其中很小一部分时，空间从 $O(n)$ 降到实际触达的节点数，这正是"隐式"的含义。配合懒标记，它支持**区间加**与**区间求和**。

### 与普通线段树的区别

1. **按需分配**: 节点指针初始为 `nil`，递归进入时才 `new` 出来，`nil` 节点代表整段为 0。
2. **区间任意**: 区间上下界只是参数，下标不必从 0 开始，也不受数组长度限制。
3. **空间**: 与实际修改/查询覆盖的节点数成正比，典型为 $O(q \log R)$（$q$ 次操作、区间跨度 $R$）。

### 懒标记（区间加）

1. **打标**: 对完全包含的节点，直接更新其 `sum` 并把增量记入 `lazy`，停止下探。
2. **下传**: 再次访问该节点时，把 `lazy` 分别加到左右孩子的 `sum` 与 `lazy` 上，然后清空自己。
3. **上浮**: 子节点变化后重新计算 `sum`。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// isNode 隐式线段树节点，孩子按需创建
type isNode struct {
	sum         int
	lazy        int
	left, right *isNode
}

// ImplicitSegmentTree 隐式线段树，维护区间 [lo, hi]
type ImplicitSegmentTree struct {
	lo, hi int
	root   *isNode
}

// NewImplicitSegmentTree 创建区间 [lo, hi] 的空树
func NewImplicitSegmentTree(lo, hi int) *ImplicitSegmentTree {
	return &ImplicitSegmentTree{lo: lo, hi: hi}
}

// push 对完全覆盖的节点打懒标记
func push(node *isNode, l, r, val int) {
	node.sum += (r - l + 1) * val
	node.lazy += val
}

// pushDown 下传懒标记，必要时创建孩子
func pushDown(node *isNode, l, r int) {
	if node.lazy == 0 || l == r {
		node.lazy = 0
		return
	}
	mid := (l + r) / 2
	if node.left == nil {
		node.left = &isNode{}
	}
	if node.right == nil {
		node.right = &isNode{}
	}
	push(node.left, l, mid, node.lazy)
	push(node.right, mid+1, r, node.lazy)
	node.lazy = 0
}

// Update 把区间 [ql, qr] 的所有元素加上 val
func (t *ImplicitSegmentTree) Update(ql, qr, val int) {
	var rec func(pp **isNode, l, r int)
	rec = func(pp **isNode, l, r int) {
		if ql > r || qr < l {
			return
		}
		if *pp == nil {
			*pp = &isNode{}
		}
		node := *pp
		if ql <= l && r <= qr {
			push(node, l, r, val)
			return
		}
		pushDown(node, l, r)
		mid := (l + r) / 2
		rec(&node.left, l, mid)
		rec(&node.right, mid+1, r)
		node.sum = 0
		if node.left != nil {
			node.sum += node.left.sum
		}
		if node.right != nil {
			node.sum += node.right.sum
		}
	}
	rec(&t.root, t.lo, t.hi)
}

// Query 求区间 [ql, qr] 的和
func (t *ImplicitSegmentTree) Query(ql, qr int) int {
	var rec func(node *isNode, l, r int) int
	rec = func(node *isNode, l, r int) int {
		if node == nil || ql > r || qr < l {
			return 0
		}
		if ql <= l && r <= qr {
			return node.sum
		}
		pushDown(node, l, r)
		mid := (l + r) / 2
		return rec(node.left, l, mid) + rec(node.right, mid+1, r)
	}
	return rec(t.root, t.lo, t.hi)
}

// countNodes 统计实际创建的节点数
func countNodes(n *isNode) int {
	if n == nil {
		return 0
	}
	return 1 + countNodes(n.left) + countNodes(n.right)
}

func main() {
	// 维护一个跨度超过 10 亿的"稀疏"区间
	t := NewImplicitSegmentTree(0, 1<<30-1)

	t.Update(100, 199, 5)  // [100,199] 每个元素 +5
	t.Update(150, 299, 3)  // [150,299] 每个元素 +3

	fmt.Println("全区间和:", t.Query(0, 1<<30-1)) // 950
	fmt.Println("区间[100,149]和:", t.Query(100, 149))
	fmt.Println("区间[150,199]和:", t.Query(150, 199))
	fmt.Println("实际创建节点数:", countNodes(t.root))
}
```

运行输出：

```text
全区间和: 950
区间[100,149]和: 250
区间[150,199]和: 400
实际创建节点数: 59
```

### 复杂度分析

- **区间更新/查询**: $O(\log (hi-lo+1))$，只沿两条路径下行。
- **空间**: $O(q \log R)$，与操作次数 $q$ 和区间跨度的对数相关，而不是区间跨度本身。
- **初始化**: $O(1)$，无需预分配。

### 应用场景

- 下标范围极大但极稀疏的区间修改（如 $[1, 10^9]$ 上的随机单点修改）。
- 动开线段树、可持久化线段树的建树基础。

### 总结

隐式线段树把"空间"也变成了按需付费：节点只有被触达才会存在，懒标记则保证区间更新仍然 $O(\log n)$。当区间跨度远大于实际操作数时，它比预分配的普通线段树划算得多。
