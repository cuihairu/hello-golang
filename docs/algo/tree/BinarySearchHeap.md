# 二叉搜索堆

二叉搜索堆是一种"双关键字"二叉树：每个节点同时携带 key 和 priority，key 按二叉搜索树序排列，priority 按堆序排列。需要注意：**同一个关键字不可能同时满足 BST 序与堆序**。BST 要求右孩子大于父节点，而最大堆要求右孩子小于父节点，二者矛盾；实际结构都是用两个独立的域分别承担有序与形状两种职责（Treap 即是其随机化形式）。本篇的二叉搜索堆采用最小堆优先级，支持按 key 查找、按 priority 取极值。

### 结构性质

1. **key 满足 BST 序**: 中序遍历按 key 严格有序，支持按 key 的 $O(\log n)$ 期望查找。
2. **priority 满足最小堆序**: 根节点的 priority 是全树最小值，`Peek` 即取全局最优。
3. **root 同时是两个维度的极值入口**: 按 priority 取最值走根，按 key 查找走比较路径。

### 算法步骤

1. **Insert(key, prio)**: 按 BST 路径插入新节点；若新节点的 priority 小于父节点（破坏最小堆），旋转把它顶上去，递归直到恢复。
2. **Find(key)**: 标准 BST 查找。
3. **ExtractMin**: 取出根（priority 最小）；若有两个孩子，把 priority 较小的孩子旋上来，被取节点下沉，直到变成叶子被摘除。

### 代码示例（Go语言实现）

```go
package main

import "fmt"

// BSHNode 二叉搜索堆节点
type BSHNode struct {
	Key      int
	Priority int
	Left     *BSHNode
	Right    *BSHNode
}

// rotateRight 右旋
func rotateRight(y *BSHNode) *BSHNode {
	x := y.Left
	y.Left = x.Right
	x.Right = y
	return x
}

// rotateLeft 左旋
func rotateLeft(x *BSHNode) *BSHNode {
	y := x.Right
	x.Right = y.Left
	y.Left = x
	return y
}

// Insert 按 key 插入，priority 破坏最小堆时旋转修复
func Insert(n *BSHNode, key, prio int) *BSHNode {
	if n == nil {
		return &BSHNode{Key: key, Priority: prio}
	}
	if key < n.Key {
		n.Left = Insert(n.Left, key, prio)
		if n.Left.Priority < n.Priority {
			n = rotateRight(n)
		}
	} else if key > n.Key {
		n.Right = Insert(n.Right, key, prio)
		if n.Right.Priority < n.Priority {
			n = rotateLeft(n)
		}
	}
	return n
}

// Find 按 key 查找
func Find(n *BSHNode, key int) bool {
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

// Peek 查看 priority 最小的节点（根）
func Peek(n *BSHNode) (int, int, bool) {
	if n == nil {
		return 0, 0, false
	}
	return n.Key, n.Priority, true
}

// extractMinNode 摘掉 n 子树的根节点，返回剩余部分
func extractMinNode(n *BSHNode) *BSHNode {
	if n == nil {
		return nil
	}
	if n.Left == nil {
		return n.Right
	}
	if n.Right == nil {
		return n.Left
	}
	// 两个孩子：把 priority 较小的孩子旋上来，让被摘节点下沉
	if n.Left.Priority < n.Right.Priority {
		n = rotateRight(n)
		n.Right = extractMinNode(n.Right)
	} else {
		n = rotateLeft(n)
		n.Left = extractMinNode(n.Left)
	}
	return n
}

// InOrder 按 key 中序遍历
func InOrder(n *BSHNode, out *[]int) {
	if n == nil {
		return
	}
	InOrder(n.Left, out)
	*out = append(*out, n.Key)
	InOrder(n.Right, out)
}

func main() {
	// (key, priority) 数据对
	pairs := [][2]int{
		{5, 30}, {2, 10}, {8, 25},
		{1, 50}, {4, 15}, {7, 60}, {9, 45},
	}
	var root *BSHNode
	for _, p := range pairs {
		root = Insert(root, p[0], p[1])
	}

	var out []int
	InOrder(root, &out)
	fmt.Println("按 key 有序:", out)

	k, prio, ok := Peek(root)
	fmt.Println("priority 最小: key =", k, ", priority =", prio, ", ok =", ok)
	fmt.Println("查找 key=4:", Find(root, 4))
	fmt.Println("查找 key=100:", Find(root, 100))

	// 按 priority 从小到大依次取出
	for root != nil {
		k, prio, _ := Peek(root)
		fmt.Printf("取出 key=%d priority=%d\n", k, prio)
		root = extractMinNode(root)
	}
}
```

运行输出：

```text
按 key 有序: [1 2 4 5 7 8 9]
priority 最小: key = 2 , priority = 10 , ok = true
查找 key=4: true
查找 key=100: false
取出 key=2 priority=10
取出 key=4 priority=15
取出 key=8 priority=25
取出 key=5 priority=30
取出 key=9 priority=45
取出 key=1 priority=50
取出 key=7 priority=60
```

### 复杂度分析

- **Insert / Find / ExtractMin**: 期望 $O(\log n)$，最坏 $O(n)$。
- **Peek**: $O(1)$。
- **空间**: $O(n)$。

### 总结

二叉搜索堆的关键在于用两个关键字分工：key 承担有序性，priority 承担形状。它把"按 key 查找"和"按优先级取最值"合并在同一棵树上，Treap、笛卡尔树都属于这一类双关键字结构。
