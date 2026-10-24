# Full Binary Tree

A full binary tree (Full/Perfect Binary Tree) is a binary tree where "every level is completely filled": a full binary tree of height $h$ has exactly $2^h - 1$ nodes, and level $i$ (counting from 0) has exactly $2^i$ nodes. In English usage, "full binary tree" sometimes means "every node is either a leaf or has two children" (a strict binary tree); this page follows the "every level filled" meaning common in Chinese textbooks, and the code verifies both properties at once.

### Properties

1. **Node count**: a full binary tree of height $h$ has $2^h - 1$ nodes in total.
2. **Leaf count**: level $h-1$ holds $2^{h-1}$ leaves, half of all nodes.
3. **Numbering relation**: numbered in level order $1..2^h-1$, the parent of node $i$ is $\lfloor i/2 \rfloor$ and its children are $2i$ and $2i+1$.

### Algorithm Steps (building and verifying)

1. **Build**: build recursively from a level-order array; index `i` has children `2i+1` and `2i+2`, and an array used up exactly yields a full binary tree.
2. **Count per level**: BFS records the node count of each level, verifying that level `i` has $2^i$ nodes.
3. **Verify the total node count**: `count == (1 << height) - 1`.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// BNode is a binary tree node
type BNode struct {
	Val   int
	Left  *BNode
	Right *BNode
}

// build builds a binary tree from a level-order array (a fully used array gives a full binary tree)
func build(values []int, i int) *BNode {
	if i >= len(values) {
		return nil
	}
	return &BNode{
		Val:   values[i],
		Left:  build(values, 2*i+1),
		Right: build(values, 2*i+2),
	}
}

// levelSizes returns the node count of each level
func levelSizes(root *BNode) []int {
	var sizes []int
	queue := []*BNode{root}
	for len(queue) > 0 {
		n := len(queue)
		sizes = append(sizes, n)
		var next []*BNode
		for _, node := range queue {
			if node.Left != nil {
				next = append(next, node.Left)
			}
			if node.Right != nil {
				next = append(next, node.Right)
			}
		}
		queue = next
	}
	return sizes
}

// count counts the total number of nodes
func count(root *BNode) int {
	if root == nil {
		return 0
	}
	return 1 + count(root.Left) + count(root.Right)
}

func main() {
	// a full binary tree of height 3, 7 nodes in total
	root := build([]int{1, 2, 3, 4, 5, 6, 7}, 0)

	sizes := levelSizes(root)
	fmt.Println("nodes per level:", sizes) // [1 2 4]

	height := len(sizes)
	fmt.Println("height:", height)
	fmt.Println("total nodes:", count(root), "expected:", (1<<height)-1)

	// cross-check: level i should have 2^i nodes
	ok := true
	for i, s := range sizes {
		if s != 1<<i {
			ok = false
		}
	}
	fmt.Println("is a full binary tree:", ok)
}
```

Output:

```text
nodes per level: [1 2 4]
height: 3
total nodes: 7 expected: 7
is a full binary tree: true
```

### Complexity Analysis

- **Build/traverse/count**: $O(n)$, where $n = 2^h - 1$ is the total number of nodes.
- **Space**: recursion depth $O(h) = O(\log n)$.

### Summary

A full binary tree is the most "orderly" binary tree in shape: node count, level count and child positions are all fixed exponential relations. It is the baseline shape used when analyzing the space upper bound of structures such as heaps and segment trees, and the reference point for concepts like the complete binary tree and the strict binary tree.

## References

- [Binary tree · Wikipedia](https://en.wikipedia.org/wiki/Binary_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [FenwickTree](/algo/tree/FenwickTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FenwickTree](/algo/tree/FenwickTree.md)
