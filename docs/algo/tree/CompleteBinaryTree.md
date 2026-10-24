# Complete Binary Tree

A complete binary tree (Complete Binary Tree) is a binary tree that is "only allowed to be missing nodes on the right of the last level": every level except the last is filled, and the nodes on the last level must be arranged contiguously from left to right. This property lets it be stored compactly in an array without wasting space — a binary heap is built on exactly this property.

### Properties

1. **The most space-efficient binary tree of its height**: there are no "hole" nodes.
2. **Array representation**: stored in an array in level order, the left child of index `i` is `2i+1`, the right child is `2i+2`, the parent is `(i-1)/2`, and no holes ever appear in the array.
3. **Height**: $O(\log n)$; a complete binary tree with $n$ nodes has height $\lfloor \log_2 n \rfloor$.

### Algorithm Steps (checking for a complete binary tree)

1. Do a level-order traversal (BFS) of the tree, enqueueing `nil` children too.
2. As soon as a `nil` is seen, set `seenNil = true`.
3. If a non-nil node appears after `seenNil`, there is a hole on the left and the tree is not complete.

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

// isComplete checks whether the binary tree is a complete binary tree
func isComplete(root *BNode) bool {
	if root == nil {
		return true
	}
	queue := []*BNode{root}
	seenNil := false
	for len(queue) > 0 {
		node := queue[0]
		queue = queue[1:]
		if node == nil {
			seenNil = true
			continue
		}
		if seenNil {
			return false // a node appeared after a hole
		}
		queue = append(queue, node.Left, node.Right)
	}
	return true
}

// build builds a binary tree from a level-order array
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

func main() {
	complete := build([]int{1, 2, 3, 4, 5, 6}, 0)
	fmt.Println("tree1 complete:", isComplete(complete))

	// 3 has no left child but does have a right one, breaking "contiguous from left to right"
	notComplete := &BNode{
		Val:   1,
		Left:  &BNode{Val: 2},
		Right: &BNode{Val: 3, Right: &BNode{Val: 6}},
	}
	fmt.Println("tree2 complete:", isComplete(notComplete))
}
```

Output:

```text
tree1 complete: true
tree2 complete: false
```

### Complexity Analysis

- **Completeness check**: $O(n)$ time, $O(n)$ queue space.
- **Parent/child access in the array representation**: $O(1)$ (pure index arithmetic).

### Use Cases

- The underlying shape of binary heaps / priority queues.
- Heapsort, and array-style storage for segment trees.

### Summary

The whole point of a complete binary tree is "no holes", which is why it maps losslessly onto an array and the parent/child relation can be expressed with index arithmetic alone. The key to checking completeness is spotting that "no non-nil node may follow a nil node".

## References

- [Binary tree · Wikipedia](https://en.wikipedia.org/wiki/Binary_tree)
- [Binary heap · Wikipedia](https://en.wikipedia.org/wiki/Binary_heap)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [BinaryTree](/algo/tree/BinaryTree.md)
- [FenwickTree](/algo/tree/FenwickTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BinaryTree](/algo/tree/BinaryTree.md)
- [FenwickTree](/algo/tree/FenwickTree.md)
