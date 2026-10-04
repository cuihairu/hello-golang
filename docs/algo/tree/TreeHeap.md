# 树堆

树堆（Tree Heap，即 Treap 的"树 + 堆"本义）是指同时满足二叉搜索树序与堆序的二叉树结构。本篇用它最经典的"无旋"实现展开：插入、删除只靠 **Split（分裂）** 与 **Merge（合并）** 两个操作，不涉及旋转。

### 两条约束

1. **BST 序**: 中序遍历按 key 有序。
2. **堆序**: 节点 priority 大于等于子节点（最大堆），优先级高的节点离根近。

### 核心操作

1. **Split(n, k)**: 把树按 key 分裂成两棵：所有 `key < k` 的节点在左树，其余在右树。
2. **Merge(a, b)**: 合并两棵树，要求左树所有 key 小于右树所有 key；比较两根的 priority，priority 高的当根，递归合并它的一侧。
3. **Insert**: `Split` 出左右，把新节点夹在中间连续 `Merge` 两次。
4. **Delete**: `Split(root, key)` 得到 `<key` 与 `>=key`，再对后者 `Split(root, key+1)` 分出 `==key` 与 `>key`，丢弃中间，合并两侧。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"math/rand"
)

// TreeHeapNode 树堆节点：Key 按 BST 序，Priority 按最大堆序
type TreeHeapNode struct {
	Key      int
	Priority int
	Left     *TreeHeapNode
	Right    *TreeHeapNode
}

// Split 把树分裂为（key < k）与（key >= k）两棵
func Split(n *TreeHeapNode, k int) (*TreeHeapNode, *TreeHeapNode) {
	if n == nil {
		return nil, nil
	}
	if n.Key < k {
		l, r := Split(n.Right, k)
		n.Right = l
		return n, r
	}
	l, r := Split(n.Left, k)
	n.Left = r
	return l, n
}

// Merge 合并两棵树（左树所有 key < 右树所有 key）
func Merge(a, b *TreeHeapNode) *TreeHeapNode {
	if a == nil {
		return b
	}
	if b == nil {
		return a
	}
	if a.Priority > b.Priority {
		a.Right = Merge(a.Right, b)
		return a
	}
	b.Left = Merge(a, b.Left)
	return b
}

// Find 查找 key 是否存在
func Find(n *TreeHeapNode, key int) bool {
	for n != nil {
		if key == n.Key {
			return true
		} else if key < n.Key {
			n = n.Left
		} else {
			n = n.Right
		}
	}
	return false
}

// Insert 插入 key（重复键忽略）
func Insert(n *TreeHeapNode, key, prio int) *TreeHeapNode {
	if Find(n, key) {
		return n
	}
	l, r := Split(n, key)
	return Merge(Merge(l, &TreeHeapNode{Key: key, Priority: prio}), r)
}

// Delete 删除 key
func Delete(n *TreeHeapNode, key int) *TreeHeapNode {
	l, m := Split(n, key)      // m 中 key >= 本 key
	_, r := Split(m, key+1)    // r 中 key > 本 key，中间恰为 key
	return Merge(l, r)
}

// InOrder 中序遍历
func InOrder(n *TreeHeapNode, out *[]int) {
	if n == nil {
		return
	}
	InOrder(n.Left, out)
	*out = append(*out, n.Key)
	InOrder(n.Right, out)
}

// checkHeap 校验最大堆性质
func checkHeap(n *TreeHeapNode) bool {
	if n == nil {
		return true
	}
	if n.Left != nil && n.Left.Priority > n.Priority {
		return false
	}
	if n.Right != nil && n.Right.Priority > n.Priority {
		return false
	}
	return checkHeap(n.Left) && checkHeap(n.Right)
}

func main() {
	rng := rand.New(rand.NewSource(7))
	var root *TreeHeapNode
	for _, k := range []int{1, 2, 3, 4, 5, 6, 7, 8, 9} {
		root = Insert(root, k, rng.Intn(1<<30))
	}

	var out []int
	InOrder(root, &out)
	fmt.Println("中序遍历:", out)
	fmt.Println("堆序合法:", checkHeap(root))

	root = Delete(root, 5)
	out = nil
	InOrder(root, &out)
	fmt.Println("删除 5 后:", out)
	fmt.Println("查找 5:", Find(root, 5))
	fmt.Println("堆序合法:", checkHeap(root))
}
```

运行输出：

```text
中序遍历: [1 2 3 4 5 6 7 8 9]
堆序合法: true
删除 5 后: [1 2 3 4 6 7 8 9]
查找 5: false
堆序合法: true
```

### 复杂度分析

- **Split / Merge**: 期望 $O(\log n)$（随机构造下）。
- **Insert / Delete**: 一次 Split 加一到两次 Merge，期望 $O(\log n)$。
- **空间**: $O(n)$。

### 总结

树堆的无旋实现把平衡树的操作收敛为"分裂 + 合并"两条原语，插入和删除都不用旋转，区间操作、可持久化这类扩展也建立在这两条原语上。
