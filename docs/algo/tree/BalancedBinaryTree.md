# 平衡二叉树

平衡二叉树（Balanced Binary Tree）泛指左右子树高度差有严格限制的二叉树，最典型的是 AVL 树：任意节点左右子树的高度差（平衡因子）的绝对值不超过 1。高度上的约束保证了树高始终是 $O(\log n)$，查找、插入、删除因此稳定在 $O(\log n)$。

### 核心概念

1. **平衡因子**: `bf = height(left) - height(right)`，取值只能是 $-1、0、1$。
2. **失衡四种情形**:
   - **LL**: 左孩子的左子树过高，右旋一次；
   - **RR**: 右孩子的右子树过高，左旋一次；
   - **LR**: 左孩子的右子树过高，先左旋左孩子，再右旋；
   - **RL**: 右孩子的左子树过高，先右旋右孩子，再左旋。
3. **维护**: 每次插入/删除后沿路径回溯更新高度，发现失衡即旋转修复，插入最多一次旋转，删除最多 $O(\log n)$ 次。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// AVLNode AVL 树节点
type AVLNode struct {
	Key    int
	Height int
	Left   *AVLNode
	Right  *AVLNode
}

func newNode(key int) *AVLNode {
	return &AVLNode{Key: key, Height: 1}
}

func height(n *AVLNode) int {
	if n == nil {
		return 0
	}
	return n.Height
}

// update 更新节点高度
func update(n *AVLNode) {
	lh, rh := height(n.Left), height(n.Right)
	if lh > rh {
		n.Height = lh + 1
	} else {
		n.Height = rh + 1
	}
}

// balanceFactor 计算平衡因子
func balanceFactor(n *AVLNode) int {
	return height(n.Left) - height(n.Right)
}

// rightRotate 右旋
func rightRotate(y *AVLNode) *AVLNode {
	x := y.Left
	t2 := x.Right
	x.Right = y
	y.Left = t2
	update(y)
	update(x)
	return x
}

// leftRotate 左旋
func leftRotate(x *AVLNode) *AVLNode {
	y := x.Right
	t2 := y.Left
	y.Left = x
	x.Right = t2
	update(x)
	update(y)
	return y
}

// Insert 插入并恢复平衡，返回新子树根
func (n *AVLNode) Insert(key int) *AVLNode {
	if n == nil {
		return newNode(key)
	}
	if key < n.Key {
		n.Left = n.Left.Insert(key)
	} else if key > n.Key {
		n.Right = n.Right.Insert(key)
	} else {
		return n // 重复键忽略
	}
	update(n)
	bf := balanceFactor(n)

	// LL
	if bf > 1 && key < n.Left.Key {
		return rightRotate(n)
	}
	// RR
	if bf < -1 && key > n.Right.Key {
		return leftRotate(n)
	}
	// LR
	if bf > 1 && key > n.Left.Key {
		n.Left = leftRotate(n.Left)
		return rightRotate(n)
	}
	// RL
	if bf < -1 && key < n.Right.Key {
		n.Right = rightRotate(n.Right)
		return leftRotate(n)
	}
	return n
}

// InOrder 中序遍历
func (n *AVLNode) InOrder(out *[]int) {
	if n == nil {
		return
	}
	n.Left.InOrder(out)
	*out = append(*out, n.Key)
	n.Right.InOrder(out)
}

// isBalanced 检查所有节点的平衡因子是否都在 [-1, 1]
func isBalanced(n *AVLNode) bool {
	if n == nil {
		return true
	}
	bf := balanceFactor(n)
	if bf < -1 || bf > 1 {
		return false
	}
	return isBalanced(n.Left) && isBalanced(n.Right)
}

func main() {
	var root *AVLNode
	// 有序插入会连续触发 RR 旋转
	for _, k := range []int{10, 20, 30, 40, 50, 25} {
		root = root.Insert(k)
	}

	var out []int
	root.InOrder(&out)
	fmt.Println("中序遍历:", out)
	fmt.Println("是否平衡:", isBalanced(root))
	fmt.Println("根节点:", root.Key)
	fmt.Println("高度:", root.Height)
}
```

运行输出：

```text
中序遍历: [10 20 25 30 40 50]
是否平衡: true
根节点: 30
高度: 3
```

### 复杂度分析

- **查找/插入/删除**: $O(\log n)$（树高被平衡因子限制在 $1.44 \log n$ 以内）。
- **空间**: $O(n)$。

### 总结

AVL 树通过"高度 + 旋转"把平衡性变成硬约束，查询性能在各类平衡树中最优；代价是插入删除的旋转维护较多。它是理解红黑树、B 树等更强工程化结构的入门样板。
