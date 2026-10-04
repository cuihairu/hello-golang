## 二叉树

二叉树（Binary Tree）的每个节点最多有两个子节点，分别叫左子节点和右子节点。表达式解析、排序算法和搜索算法里都用得到它。

### 常见术语

1. **节点（Node）**：树的基本单位，包含数据和指向子节点的指针。
2. **边（Edge）**：连接两个节点的线段。
3. **度（Degree）**：一个节点的子节点数。
4. **根节点（Root Node）**：树的顶端节点，没有父节点。
5. **叶节点（Leaf Node）**：没有子节点的节点。
6. **父节点（Parent Node）**：具有子节点的节点。
7. **子节点（Child Node）**：由另一个节点指向的节点。
8. **节点高度（Node Height）**：从当前节点到叶节点的最长路径上的边数。
9. **树的高度（Tree Height）**：树中节点的最大高度。
10. **深度（Depth）**：从根节点到当前节点的路径上的边数。
11. **完全二叉树（Complete Binary Tree）**：除最后一层外，每一层的所有节点都有两个子节点，最后一层的节点尽可能左对齐。
12. **满二叉树（Full Binary Tree）**：所有非叶节点都有两个子节点，所有叶节点在同一层。
13. **完美二叉树（Perfect Binary Tree）**：一个满二叉树，同时也是完全二叉树。

### 前序遍历、中序遍历和后序遍历的特点比较

| 遍历方式 | 访问顺序 | 特点 |
|---------|---------|------|
| 前序遍历（Pre-order） | 根节点 -> 左子树 -> 右子树 | 先访问根节点，适合用于复制二叉树 |
| 中序遍历（In-order）  | 左子树 -> 根节点 -> 右子树 | 中序遍历二叉搜索树可得到有序序列 |
| 后序遍历（Post-order）| 左子树 -> 右子树 -> 根节点 | 先访问子节点，适合用于删除二叉树 |

### 二叉树的基本操作

二叉树的常见操作是插入、查找、删除和三种遍历（前序、中序、后序），树高和节点高度也常要算。下面的实现覆盖插入、遍历和高度计算。

### Go语言实现二叉树

```go
package main

import "fmt"

// 定义节点结构体
type TreeNode struct {
    Value int
    Left  *TreeNode
    Right *TreeNode
}

// 插入节点
func (n *TreeNode) Insert(value int) {
    if n == nil {
        return
    } else if value <= n.Value {
        if n.Left == nil {
            n.Left = &TreeNode{Value: value}
        } else {
            n.Left.Insert(value)
        }
    } else {
        if n.Right == nil {
            n.Right = &TreeNode{Value: value}
        } else {
            n.Right.Insert(value)
        }
    }
}

// 前序遍历
func (n *TreeNode) PreOrderTraversal() {
    if n == nil {
        return
    }
    fmt.Printf("%d ", n.Value)
    n.Left.PreOrderTraversal()
    n.Right.PreOrderTraversal()
}

// 中序遍历
func (n *TreeNode) InOrderTraversal() {
    if n == nil {
        return
    }
    n.Left.InOrderTraversal()
    fmt.Printf("%d ", n.Value)
    n.Right.InOrderTraversal()
}

// 后序遍历
func (n *TreeNode) PostOrderTraversal() {
    if n == nil {
        return
    }
    n.Left.PostOrderTraversal()
    n.Right.PostOrderTraversal()
    fmt.Printf("%d ", n.Value)
}

// 计算节点高度
func (n *TreeNode) NodeHeight() int {
    if n == nil {
        return -1
    }
    leftHeight := n.Left.NodeHeight()
    rightHeight := n.Right.NodeHeight()
    if leftHeight > rightHeight {
        return leftHeight + 1
    }
    return rightHeight + 1
}

// 计算树的高度
func (n *TreeNode) TreeHeight() int {
    return n.NodeHeight()
}

func main() {
    root := &TreeNode{Value: 10}
    root.Insert(5)
    root.Insert(15)
    root.Insert(2)
    root.Insert(7)
    root.Insert(12)
    root.Insert(20)

    fmt.Println("前序遍历:")
    root.PreOrderTraversal()
    fmt.Println()

    fmt.Println("中序遍历:")
    root.InOrderTraversal()
    fmt.Println()

    fmt.Println("后序遍历:")
    root.PostOrderTraversal()
    fmt.Println()

    fmt.Printf("树的高度: %d\n", root.TreeHeight())
}
```

### 代码解释

1. **定义节点结构体**：`TreeNode`结构体包含节点的值以及指向左子节点和右子节点的指针。
2. **插入节点**：`Insert`方法根据值的大小将新节点插入到二叉树的适当位置。
3. **前序遍历**：`PreOrderTraversal`方法先访问节点本身，然后递归遍历左子树和右子树。
中序和后序的差别只在访问节点本身的时机：中序把访问夹在两次子树递归之间，后序放到最后。`NodeHeight` 递归取左右子树高度的较大值加一，`TreeHeight` 返回根节点的高度。

插入、遍历、算高度是二叉树的基本操作。前面的表定下了三种遍历各自的用途：中序给二叉搜索树排出有序序列，前序适合复制，后序适合删除。

### 复杂度

三种遍历都把每个节点恰好访问一次，时间 O(n)，递归深度等于树高 h，栈空间 O(h)。插入沿一条从根到叶的路径走，O(h)。普通二叉树对形状没有约束，h 最坏退到 n-1（节点连成一条链），插入和查找随之变成 O(n)；要把 h 稳定在 O(log n)，得靠 AVL、红黑树这类自平衡结构。