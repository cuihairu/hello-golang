## Binary Tree

Every node in a binary tree (Binary Tree) has at most two children, called the left child and the right child. It is used in expression parsing, sorting algorithms and search algorithms.

### Common Terminology

1. **Node**: the basic unit of a tree, containing data and pointers to its children.
2. **Edge**: the line segment connecting two nodes.
3. **Degree**: the number of children a node has.
4. **Root Node**: the top node of the tree, which has no parent.
5. **Leaf Node**: a node with no children.
6. **Parent Node**: a node that has children.
7. **Child Node**: a node pointed to by another node.
8. **Node Height**: the number of edges on the longest path from the current node to a leaf.
9. **Tree Height**: the maximum height among the nodes in the tree.
10. **Depth**: the number of edges on the path from the root to the current node.
11. **Complete Binary Tree**: every level except possibly the last is fully filled, and the nodes on the last level are as far left as possible.
12. **Full Binary Tree**: every non-leaf node has two children, and all leaves are on the same level.
13. **Perfect Binary Tree**: a full binary tree that is also a complete binary tree.

### Comparing the Characteristics of Pre-order, In-order and Post-order Traversals

| Traversal | Visit order | Characteristic |
|---------|---------|------|
| Pre-order | Root -> Left subtree -> Right subtree | Visits the root first, suitable for copying a binary tree |
| In-order  | Left subtree -> Root -> Right subtree | An in-order traversal of a BST yields a sorted sequence |
| Post-order | Left subtree -> Right subtree -> Root | Visits the children first, suitable for deleting a binary tree |

### Basic Operations on a Binary Tree

The common operations on a binary tree are insert, search, delete and the three traversals (pre-order, in-order, post-order); tree height and node height are also often computed. The implementation below covers insert, traversal and height calculation.

### Implementing a Binary Tree in Go

```go
package main

import "fmt"

// define the node struct
type TreeNode struct {
    Value int
    Left  *TreeNode
    Right *TreeNode
}

// insert a node
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

// pre-order traversal
func (n *TreeNode) PreOrderTraversal() {
    if n == nil {
        return
    }
    fmt.Printf("%d ", n.Value)
    n.Left.PreOrderTraversal()
    n.Right.PreOrderTraversal()
}

// in-order traversal
func (n *TreeNode) InOrderTraversal() {
    if n == nil {
        return
    }
    n.Left.InOrderTraversal()
    fmt.Printf("%d ", n.Value)
    n.Right.InOrderTraversal()
}

// post-order traversal
func (n *TreeNode) PostOrderTraversal() {
    if n == nil {
        return
    }
    n.Left.PostOrderTraversal()
    n.Right.PostOrderTraversal()
    fmt.Printf("%d ", n.Value)
}

// compute the node height
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

// compute the tree height
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

    fmt.Println("Pre-order traversal:")
    root.PreOrderTraversal()
    fmt.Println()

    fmt.Println("In-order traversal:")
    root.InOrderTraversal()
    fmt.Println()

    fmt.Println("Post-order traversal:")
    root.PostOrderTraversal()
    fmt.Println()

    fmt.Printf("Tree height: %d\n", root.TreeHeight())
}
```

### Code Explanation

1. **Define the node struct**: the `TreeNode` struct contains the node's value and pointers to the left and right children.
2. **Insert a node**: the `Insert` method inserts the new node into the right position in the binary tree based on the size of the value.
3. **Pre-order traversal**: the `PreOrderTraversal` method visits the node itself first, then recursively traverses the left and right subtrees.
The difference between in-order and post-order lies only in when the node itself is visited: in-order places the visit between the two subtree recursions, while post-order puts it last. `NodeHeight` recursively takes the larger of the left and right subtree heights and adds one, and `TreeHeight` returns the height of the root.

Insert, traversal and height calculation are the basic operations on a binary tree. The table above sets out the use of each of the three traversals: in-order produces a sorted sequence for a BST, pre-order is suitable for copying, and post-order is suitable for deleting.

### Complexity

All three traversals visit each node exactly once, giving time O(n); the recursion depth equals the tree height h, so stack space is O(h). Insert walks a single root-to-leaf path, O(h). An ordinary binary tree imposes no constraint on its shape, so h can degenerate all the way to n-1 (the nodes forming a single chain), and insert and search become O(n) as a result; to keep h steady at O(log n) you need self-balancing structures such as AVL and red-black trees.

## References

- [Binary Tree · Wikipedia](https://en.wikipedia.org/wiki/Binary_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [BinarySearchTree](/algo/tree/BinarySearchTree.md)
- [CompleteBinaryTree](/algo/tree/CompleteBinaryTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BinarySearchTree](/algo/tree/BinarySearchTree.md)
- [CompleteBinaryTree](/algo/tree/CompleteBinaryTree.md)
