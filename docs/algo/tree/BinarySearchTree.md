# Binary Search Tree

A binary search tree (Binary Search Tree, BST) is a binary tree that satisfies "every node in the left subtree < root < every node in the right subtree". This ordering constraint means search, insert and delete all need to walk down only a single path, with an average time complexity of $O(\log n)$; an in-order traversal of a BST yields a sorted sequence.

### Core Properties

1. **In-order sorted**: an in-order traversal (left-root-right) yields exactly the ascending sequence.
2. **Unique search path**: after comparing with the target you only enter one side subtree.
3. **Degeneration risk**: inserting sorted data in order degenerates the tree into a linked list, and operations degenerate to $O(n)$; balanced binary trees (AVL, red-black) exist precisely to solve this.

### Algorithm Steps

1. **Search**: if the target is less than the current node go left, if greater go right, if equal you have a hit.
2. **Insert**: follow the search path down to an empty slot and attach the new node.
3. **Delete**: three cases:
   - Leaf node: delete it directly;
   - Only one child: replace it with the child;
   - Two children: replace the node itself with the smallest node (successor) in the right subtree, then delete the successor from its original position.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// BSTNode binary search tree node
type BSTNode struct {
	Key   int
	Left  *BSTNode
	Right *BSTNode
}

// Insert inserts key (duplicates ignored), returns the new subtree root
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

// Search checks whether key exists
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

// Min returns the smallest node in the subtree
func (n *BSTNode) Min() *BSTNode {
	for n.Left != nil {
		n = n.Left
	}
	return n
}

// Delete removes key, returns the new subtree root
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
			// replace with the successor from the right subtree, then delete the successor
			succ := n.Right.Min()
			n.Key = succ.Key
			n.Right = n.Right.Delete(succ.Key)
		}
	}
	return n
}

// InOrder in-order traversal, result is ascending
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
	fmt.Println("In-order traversal:", sorted)

	fmt.Println("search 40:", root.Search(40))
	fmt.Println("search 45:", root.Search(45))

	root = root.Delete(30) // delete a node with two children
	sorted = nil
	root.InOrder(&sorted)
	fmt.Println("After deleting 30:", sorted)
}
```

Output:

```text
In-order traversal: [20 30 40 50 60 70 80]
search 40: true
search 45: false
After deleting 30: [20 40 50 60 70 80]
```

### Complexity Analysis

- **Search / insert / delete**: average $O(\log n)$, worst case $O(n)$ (when the tree degenerates into a linked list).
- **Space**: $O(n)$ for storing nodes; recursive operations have stack depth $O(h)$.

### Summary

A binary search tree moves binary search into a dynamic structure via the "left is smaller, right is larger" ordering constraint. It is simple and intuitive, and is the foundation for understanding balanced trees such as AVL and red-black; once the insertion order is unfavourable it degenerates, which is exactly the reason balanced trees exist.

## References

- [Binary Search Tree · Wikipedia](https://en.wikipedia.org/wiki/Binary_search_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [BinaryHeap](/algo/tree/BinaryHeap.md)
- [BinaryTree](/algo/tree/BinaryTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BinaryHeap](/algo/tree/BinaryHeap.md)
- [BinaryTree](/algo/tree/BinaryTree.md)
