## Introduction to the AVL Tree and a Go Implementation

### 1. What the AVL Tree Is

An AVL tree is a self-balancing binary search tree (BST), invented by Adelson-Velsky and Landis in 1962. After inserting or deleting a node, an AVL tree keeps itself balanced with rotation operations, which keeps the height always \(O(\log n)\) and so guarantees that search, insert and delete are all \(O(\log n)\) even in the worst case.

Every node carries a balance factor, which is the height of its left subtree minus the height of its right subtree. In an AVL tree each node's balance factor is only allowed to be -1, 0 or 1.

### 2. Basic AVL Tree Operations

1. **Insert a node**: inserting a node can break the AVL balance and needs rotations to restore it.
2. **Delete a node**: deleting a node can also break the balance and needs rotations to restore it.
3. **Rotations**: single left rotation, single right rotation, double left rotation and double right rotation.

### 3. AVL Tree in Go

Below is a complete AVL tree implementation, covering insert, delete, search and traversal.

```go
package main

import (
    "fmt"
)

// AVL tree node definition
type AVLNode struct {
    key    int
    height int
    left   *AVLNode
    right  *AVLNode
}

// get the height of a node
func height(n *AVLNode) int {
    if n == nil {
        return 0
    }
    return n.height
}

// get the balance factor of a node
func getBalanceFactor(n *AVLNode) int {
    if n == nil {
        return 0
    }
    return height(n.left) - height(n.right)
}

// right rotation
func rightRotate(y *AVLNode) *AVLNode {
    x := y.left
    T2 := x.right

    x.right = y
    y.left = T2

    y.height = max(height(y.left), height(y.right)) + 1
    x.height = max(height(x.left), height(x.right)) + 1

    return x
}

// left rotation
func leftRotate(x *AVLNode) *AVLNode {
    y := x.right
    T2 := y.left

    y.left = x
    x.right = T2

    x.height = max(height(x.left), height(x.right)) + 1
    y.height = max(height(y.left), height(y.right)) + 1

    return y
}

// insert a node
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

// search for a node
func search(node *AVLNode, key int) *AVLNode {
    if node == nil || node.key == key {
        return node
    }

    if key < node.key {
        return search(node.left, key)
    }
    return search(node.right, key)
}

// delete a node
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

// get the minimum value node
func minValueNode(node *AVLNode) *AVLNode {
    current := node

    for current.left != nil {
        current = current.left
    }

    return current
}

// pre-order traversal
func preOrder(node *AVLNode) {
    if node != nil {
        fmt.Printf("%d ", node.key)
        preOrder(node.left)
        preOrder(node.right)
    }
}

// helper: return the larger of two integers
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

    fmt.Println("Pre-order traversal of the AVL tree:")
    preOrder(root)
    fmt.Println()

    fmt.Println("Search for node 30:")
    node := search(root, 30)
    if node != nil {
        fmt.Printf("Found node %d\n", node.key)
    } else {
        fmt.Println("Node 30 not found")
    }

    fmt.Println("Delete node 30:")
    root = deleteNode(root, 30)
    fmt.Println("Pre-order traversal of the AVL tree:")
    preOrder(root)
    fmt.Println()
}
```

### 4. Key Points Explained

- **Height calculation**: a node's height is the taller of its left and right subtrees, plus 1.
- **Balance factor**: the height difference between the left and right subtrees.
- **Rotations**: single right, single left, double right and double left, used to restore balance.

### 5. Summary

An AVL tree clamps the balance factor to -1, 0 or 1, so the height is always \(O(\log n)\) and search, insert and delete are all \(O(\log n)\) in the worst case. The Go implementation above covers insert, delete, search and pre-order traversal, with the rotation logic concentrated in `insert` and `deleteNode`.

## References

- [AVL Tree · Wikipedia](https://en.wikipedia.org/wiki/AVL_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [Tree](/algo/tree/Tree.md)
- [B+Tree](/algo/tree/B+Tree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [B+Tree](/algo/tree/B+Tree.md)
- [Tree](/algo/tree/Tree.md)
