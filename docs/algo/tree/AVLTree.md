## AVL 树简介及 Go 实现

### 1. AVL 树简介

AVL 树是一种自平衡二叉搜索树（Binary Search Tree，BST），由 Adelson-Velsky 和 Landis 于1962年发明。AVL 树在插入或删除节点后，通过旋转操作保持树的平衡，确保树的高度始终是 \(O(\log n)\)，从而保证了在最坏情况下，查找、插入和删除操作的时间复杂度都是 \(O(\log n)\)。

每个节点都有一个平衡因子（balance factor），它等于该节点的左子树高度减去右子树高度。AVL 树的每个节点的平衡因子只允许为 -1, 0 或 1。

### 2. AVL 树的基本操作

1. **插入节点**: 插入节点后可能会破坏 AVL 树的平衡，需要通过旋转操作来恢复平衡。
2. **删除节点**: 删除节点后也可能破坏 AVL 树的平衡，需要通过旋转操作来恢复平衡。
3. **旋转操作**: 包括单左旋、单右旋、双左旋和双右旋。

### 3. AVL 树的 Go 实现

下面是一个完整的 AVL 树实现，包括插入、删除、查找和遍历操作。

```go
package main

import (
    "fmt"
    "math"
)

// AVL树节点定义
type AVLNode struct {
    key    int
    height int
    left   *AVLNode
    right  *AVLNode
}

// 获取节点的高度
func height(n *AVLNode) int {
    if n == nil {
        return 0
    }
    return n.height
}

// 获取节点的平衡因子
func getBalanceFactor(n *AVLNode) int {
    if n == nil {
        return 0
    }
    return height(n.left) - height(n.right)
}

// 右旋转
func rightRotate(y *AVLNode) *AVLNode {
    x := y.left
    T2 := x.right

    x.right = y
    y.left = T2

    y.height = max(height(y.left), height(y.right)) + 1
    x.height = max(height(x.left), height(x.right)) + 1

    return x
}

// 左旋转
func leftRotate(x *AVLNode) *AVLNode {
    y := x.right
    T2 := y.left

    y.left = x
    x.right = T2

    x.height = max(height(x.left), height(x.right)) + 1
    y.height = max(height(y.left), height(y.right)) + 1

    return y
}

// 插入节点
func insert(node *AVLNode, key int) *AVLNode {
    if node == nil {
        return &AVLNode{key: key, height: 1}
    }

    if key < node.key {
        node.left = insert(node.left, key)
    } else if key > node.key {
        node.right = insert(node.right, key)
    } else {
        return node
    }

    node.height = 1 + max(height(node.left), height(node.right))

    balance := getBalanceFactor(node)

    if balance > 1 && key < node.left.key {
        return rightRotate(node)
    }
    if balance < -1 && key > node.right.key {
        return leftRotate(node)
    }
    if balance > 1 && key > node.left.key {
        node.left = leftRotate(node.left)
        return rightRotate(node)
    }
    if balance < -1 && key < node.right.key {
        node.right = rightRotate(node.right)
        return leftRotate(node)
    }

    return node
}

// 查找节点
func search(node *AVLNode, key int) *AVLNode {
    if node == nil || node.key == key {
        return node
    }

    if key < node.key {
        return search(node.left, key)
    }
    return search(node.right, key)
}

// 删除节点
func deleteNode(root *AVLNode, key int) *AVLNode {
    if root == nil {
        return root
    }

    if key < root.key {
        root.left = deleteNode(root.left, key)
    } else if key > root.key {
        root.right = deleteNode(root.right, key)
    } else {
        if root.left == nil {
            temp := root.right
            root = nil
            return temp
        } else if root.right == nil {
            temp := root.left
            root = nil
            return temp
        }

        temp := minValueNode(root.right)
        root.key = temp.key
        root.right = deleteNode(root.right, temp.key)
    }

    if root == nil {
        return root
    }

    root.height = 1 + max(height(root.left), height(root.right))

    balance := getBalanceFactor(root)

    if balance > 1 && getBalanceFactor(root.left) >= 0 {
        return rightRotate(root)
    }
    if balance > 1 && getBalanceFactor(root.left) < 0 {
        root.left = leftRotate(root.left)
        return rightRotate(root)
    }
    if balance < -1 && getBalanceFactor(root.right) <= 0 {
        return leftRotate(root)
    }
    if balance < -1 && getBalanceFactor(root.right) > 0 {
        root.right = rightRotate(root.right)
        return leftRotate(root)
    }

    return root
}

// 获取最小值节点
func minValueNode(node *AVLNode) *AVLNode {
    current := node

    for current.left != nil {
        current = current.left
    }

    return current
}

// 前序遍历
func preOrder(node *AVLNode) {
    if node != nil {
        fmt.Printf("%d ", node.key)
        preOrder(node.left)
        preOrder(node.right)
    }
}

// 工具函数：返回两个整数中的最大值
func max(a, b int) int {
    if a > b {
        return a
    }
    return b
}

func main() {
    var root *AVLNode

    keys := []int{10, 20, 30, 40, 50, 25}

    for _, key := range keys {
        root = insert(root, key)
    }

    fmt.Println("前序遍历AVL树：")
    preOrder(root)
    fmt.Println()

    fmt.Println("查找节点 30:")
    node := search(root, 30)
    if node != nil {
        fmt.Printf("找到节点 %d\n", node.key)
    } else {
        fmt.Println("节点 30 未找到")
    }

    fmt.Println("删除节点 30:")
    root = deleteNode(root, 30)
    fmt.Println("前序遍历AVL树：")
    preOrder(root)
    fmt.Println()
}
```

### 4. 关键点解释

- **高度计算**: 每个节点的高度等于其左右子树中高度较大的那个加1。
- **平衡因子**: 左右子树的高度差。
- **旋转操作**: 包括单右旋、单左旋、双右旋和双左旋，用于恢复平衡。

### 5. 小结

AVL 树通过严格的平衡因子限制，确保树的高度保持在 \(O(\log n)\)，从而保证了高效的查找、插入和删除操作。通过 Go 语言实现 AVL 树，可以深入理解其原理和操作。