# 二叉搜索树

二叉搜索树（Binary Search Tree, BST）是一棵满足"左子树所有节点 < 根 < 右子树所有节点"的二叉树。这一顺序约束让查找、插入、删除都只需沿一条路径下行，平均时间复杂度 $O(\log n)$；对它做中序遍历可以得到有序序列。

### 核心性质

1. **中序有序**: 中序遍历（左-根-右）恰好得到升序序列。
2. **查找路径唯一**: 与目标比较后只需进入一侧子树。
3. **退化风险**: 依序插入有序数据会退化成链表，操作退化为 $O(n)$；平衡二叉树（AVL、红黑树）正是为解决这一问题而生。

### 算法步骤

1. **查找**: 目标小于当前节点走左子树，大于走右子树，相等即命中。
2. **插入**: 沿查找路径走到空位，把新节点挂上。
3. **删除**: 分三种情况：
   - 叶子节点：直接删除；
   - 只有一个孩子：用孩子顶替；
   - 有两个孩子：用右子树的最小节点（后继）替换自身，再删除后继原位置。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// BSTNode 二叉搜索树节点
type BSTNode struct {
	Key   int
	Left  *BSTNode
	Right *BSTNode
}

// Insert 插入 key（重复值忽略），返回新的子树根
func (n *BSTNode) Insert(key int) *BSTNode {
	if n == nil {
		return &BSTNode{Key: key}
	}
	if key < n.Key {
		n.Left = n.Left.Insert(key)
	} else if key > n.Key {
		n.Right = n.Right.Insert(key)
	}
	return n
}

// Search 查找 key 是否存在
func (n *BSTNode) Search(key int) bool {
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

// Min 返回子树中最小的节点
func (n *BSTNode) Min() *BSTNode {
	for n.Left != nil {
		n = n.Left
	}
	return n
}

// Delete 删除 key，返回新的子树根
func (n *BSTNode) Delete(key int) *BSTNode {
	if n == nil {
		return nil
	}
	if key < n.Key {
		n.Left = n.Left.Delete(key)
	} else if key > n.Key {
		n.Right = n.Right.Delete(key)
	} else {
		switch {
		case n.Left == nil:
			return n.Right
		case n.Right == nil:
			return n.Left
		default:
			// 用右子树的后继替换，再删掉后继
			succ := n.Right.Min()
			n.Key = succ.Key
			n.Right = n.Right.Delete(succ.Key)
		}
	}
	return n
}

// InOrder 中序遍历，结果为升序
func (n *BSTNode) InOrder(out *[]int) {
	if n == nil {
		return
	}
	n.Left.InOrder(out)
	*out = append(*out, n.Key)
	n.Right.InOrder(out)
}

func main() {
	var root *BSTNode
	for _, k := range []int{50, 30, 70, 20, 40, 60, 80} {
		root = root.Insert(k)
	}

	var sorted []int
	root.InOrder(&sorted)
	fmt.Println("中序遍历:", sorted)

	fmt.Println("search 40:", root.Search(40))
	fmt.Println("search 45:", root.Search(45))

	root = root.Delete(30) // 删除有两个孩子的节点
	sorted = nil
	root.InOrder(&sorted)
	fmt.Println("删除 30 后:", sorted)
}
```

运行输出：

```text
中序遍历: [20 30 40 50 60 70 80]
search 40: true
search 45: false
删除 30 后: [20 40 50 60 70 80]
```

### 复杂度分析

- **查找/插入/删除**: 平均 $O(\log n)$，最坏 $O(n)$（树退化成链表时）。
- **空间**: $O(n)$ 存储节点；递归操作栈深 $O(h)$。

### 总结

二叉搜索树用"左小右大"的顺序约束把二分查找搬进了动态结构。它简单直观，是理解 AVL、红黑树、Treap 等平衡树的基础；一旦插入顺序不利就会退化，这也是平衡树存在的意义。
