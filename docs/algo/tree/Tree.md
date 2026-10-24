# Tree

A tree is a hierarchical, non-linear structure made of $n \geq 0$ nodes: there is one root node, and the remaining nodes are split into several mutually disjoint subtrees. File systems, org charts, and the DOM are all typical tree structures.

### Basic Terminology

1. **Root**: a node with no parent.
2. **Leaf**: a node with no children.
3. **Degree**: the number of children a node has.
4. **Depth**: the number of edges on the path from the root to that node.
5. **Height**: the maximum depth of any node in the tree.

### Common Operations

1. **Depth-first traversal (DFS)**: visit the root first, then recursively visit each subtree in turn (preorder).
2. **Breadth-first traversal (BFS)**: use a queue to visit nodes level by level.
3. **Compute the height**: take the maximum height among the children and add 1.

### Code Example (Go Implementation)

```go
package main

import (
	"fmt"
	"strings"
)

// TreeNode tree node; Children holds all of its children
type TreeNode struct {
	Val      string
	Children []*TreeNode
}

// AddChild adds a child node
func (n *TreeNode) AddChild(child *TreeNode) {
	n.Children = append(n.Children, child)
}

// DepthFirst depth-first traversal (preorder)
func DepthFirst(node *TreeNode, depth int) {
	if node == nil {
		return
	}
	fmt.Printf("%s- %s\n", strings.Repeat("  ", depth), node.Val)
	for _, c := range node.Children {
		DepthFirst(c, depth+1)
	}
}

// BreadthFirst breadth-first traversal (level by level)
func BreadthFirst(root *TreeNode) {
	queue := []*TreeNode{root}
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		fmt.Printf("%s ", node.Val)
		queue = append(queue, node.Children...)
	}
	fmt.Println()
}

// Height computes the height of the tree (counted in nodes)
func Height(node *TreeNode) int {
	if node == nil {
		return 0
	}
	best := 0
	for _, c := range node.Children {
		if h := Height(c); h > best {
			best = h
		}
	}
	return best + 1
}

func main() {
	root := &TreeNode{Val: "Company"}
	rd := &TreeNode{Val: "R&D"}
	mkt := &TreeNode{Val: "Marketing"}
	root.AddChild(rd)
	root.AddChild(mkt)
	rd.AddChild(&TreeNode{Val: "Frontend"})
	rd.AddChild(&TreeNode{Val: "Backend"})

	DepthFirst(root, 0)
	BreadthFirst(root)
	fmt.Println("height:", Height(root))
}
```

Output:

```text
- Company
  - R&D
    - Frontend
    - Backend
  - Marketing
Company R&D Marketing Frontend Backend 
height: 3
```

### Complexity Analysis

- **Traversal**: $O(n)$, each node visited once; BFS additionally needs $O(w)$ queue space ($w$ is the maximum width).
- **Height**: $O(n)$.
- **Storage**: each node keeps a slice of child pointers, so total space is $O(n)$.

### Summary

A tree expresses "one-to-many" hierarchical relationships as a collection of child pointers, and describing tree operations with recursion is usually the most natural way. Binary trees, heaps, and tries are all special cases of it, and later chapters will expand on them one by one.

## References

- [Tree (data structure) · Wikipedia](https://en.wikipedia.org/wiki/Tree_%28data_structure%29))


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [SegmentTree](/algo/tree/SegmentTree.md)
- [AVLTree](/algo/tree/AVLTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AVLTree](/algo/tree/AVLTree.md)
- [SegmentTree](/algo/tree/SegmentTree.md)
