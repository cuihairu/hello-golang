# Treap

Treap 是 Tree + Heap 的合成词：每个节点同时携带 **key** 和 **priority**，key 按二叉搜索树的规则排列，priority 按堆的规则排列。由于 BST 序与堆序各自约束一条链，固定 key 后随机化的 priority（相当于随机化插入顺序）就把树高控制在期望 $O(\log n)$。

### 性质

1. **BST 序**: 中序遍历（按 key）严格有序。
2. **堆序**: 任意节点的 priority 都小于等于父节点（最大堆）。
3. **唯一形态**: 给定 key 与 priority 后，树的形态唯一确定（等价于按 priority 降序插入的 BST）。

### 核心操作（旋转实现）

1. **Insert**: 先按 key 找到空位插入；若新节点的 priority 大于父节点，通过旋转把它"顶"上去，递归直到堆序恢复。
2. **Delete**: 找到节点；若是叶子直接摘除；若只有一个孩子用孩子顶替；若有两个孩子，把 priority 较高的孩子旋转上来（使被删节点下沉），递归删除，直到退化为前两种情况。

### 代码示例（Go语言实现）

```go
package main

import (
	"fmt"
	"math/rand"
)

// TreapNode 双关键字节点
type TreapNode struct {
	Key      int
	Priority int
	Left     *TreapNode
	Right    *TreapNode
}

// rotateRight 右旋
func rotateRight(y *TreapNode) *TreapNode {
	x := y.Left
	y.Left = x.Right
	x.Right = y
	return x
}

// rotateLeft 左旋
func rotateLeft(x *TreapNode) *TreapNode {
	y := x.Right
	x.Right = y.Left
	y.Left = x
	return y
}

// Insert 插入 key，返回新子树根
func Insert(n *TreapNode, key, prio int) *TreapNode {
	if n == nil {
		return &TreapNode{Key: key, Priority: prio}
	}
	if key < n.Key {
		n.Left = Insert(n.Left, key, prio)
		if n.Left.Priority > n.Priority {
			n = rotateRight(n)
		}
	} else if key > n.Key {
		n.Right = Insert(n.Right, key, prio)
		if n.Right.Priority > n.Priority {
			n = rotateLeft(n)
		}
	}
	return n
}

// Delete 删除 key，返回新子树根
func Delete(n *TreapNode, key int) *TreapNode {
	if n == nil {
		return nil
	}
	if key < n.Key {
		n.Left = Delete(n.Left, key)
	} else if key > n.Key {
		n.Right = Delete(n.Right, key)
	} else {
		// 叶子或只有一个孩子
		if n.Left == nil {
			return n.Right
		}
		if n.Right == nil {
			return n.Left
		}
		// 两个孩子：把 priority 较高的孩子旋上来，让被删节点下沉
		if n.Left.Priority > n.Right.Priority {
			n = rotateRight(n)
			n.Right = Delete(n.Right, key)
		} else {
			n = rotateLeft(n)
			n.Left = Delete(n.Left, key)
		}
	}
	return n
}

// InOrder 中序遍历
func InOrder(n *TreapNode, out *[]int) {
	if n == nil {
		return
	}
	InOrder(n.Left, out)
	*out = append(*out, n.Key)
	InOrder(n.Right, out)
}

// checkBST 校验 BST 序与堆序
func checkBST(n *TreapNode, lo, hi int) bool {
	if n == nil {
		return true
	}
	if n.Key <= lo || n.Key >= hi {
		return false
	}
	return checkBST(n.Left, lo, n.Key) && checkBST(n.Right, n.Key, hi)
}

func checkHeap(n *TreapNode) bool {
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
	rng := rand.New(rand.NewSource(42))
	var root *TreapNode
	keys := []int{5, 3, 8, 1, 4, 7, 9, 2, 6}
	for _, k := range keys {
		root = Insert(root, k, rng.Intn(1<<30))
	}

	var out []int
	InOrder(root, &out)
	fmt.Println("中序遍历:", out)
	fmt.Println("BST 序合法:", checkBST(root, -1<<60, 1<<60))
	fmt.Println("堆序合法:", checkHeap(root))

	root = Delete(root, 3)
	root = Delete(root, 8)
	out = nil
	InOrder(root, &out)
	fmt.Println("删除 3 和 8 后:", out)
	fmt.Println("BST 序合法:", checkBST(root, -1<<60, 1<<60))
	fmt.Println("堆序合法:", checkHeap(root))
}
```

运行输出：

```text
中序遍历: [1 2 3 4 5 6 7 8 9]
BST 序合法: true
堆序合法: true
删除 3 和 8 后: [1 2 4 5 6 7 9]
BST 序合法: true
堆序合法: true
```

### 复杂度分析

- **查找/插入/删除**: 期望 $O(\log n)$，最坏 $O(n)$（随机 priority 极端时）。
- **空间**: $O(n)$。

### 总结

Treap 把“平衡”交给随机数：key 负责有序，priority 负责形状，旋转只在破坏堆序时发生。竞赛和工程里要一棵支持分裂合并的平衡树时，它常被拿来当底座。
