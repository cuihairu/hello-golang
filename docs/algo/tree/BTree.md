# B Tree

A B tree (B-Tree) is a multi-way balanced search tree, designed for block storage such as disks: each node can hold several keys and several child pointers, so reading a whole node at once performs a multi-way comparison and cuts down the number of I/O operations substantially. Database indexes (such as MySQL InnoDB) are a typical application of the B tree family.

### Structural Constraints (minimum degree t)

1. Each node has at most $2t-1$ keys and $2t$ children.
2. Apart from the root, each node has at least $t-1$ keys and $t$ children.
3. Keys are ascending within a node, and a parent node's keys partition the key ranges of its subtrees.
4. All leaves are on the same level — a B tree grows "half-full from the leaves upward", and inserts keep it balanced via **node splitting**.

### Algorithm Steps (Insert)

1. **Insert into a non-full node**: walk down by key; a leaf inserts directly while staying sorted; an internal node picks the right subtree and keeps walking down.
2. **Split early**: on the way down, split any "full node" ($2t-1$ keys) immediately — the middle key moves up to the parent, and the left and right halves become two new children; then pick one half and keep inserting.
3. **Split the root**: when the root is full, create a new root holding only the old root, and after the split the height grows by one — this is how a B tree "grows upward" while keeping all leaves on the same level.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// BTreeNode B tree node
type BTreeNode struct {
	keys     []int        // keys, ascending
	children []*BTreeNode // child pointers, length len(keys)+1; empty for leaves
	leaf     bool
}

// BTree a B tree with minimum degree t, at most 2t-1 keys per node
type BTree struct {
	root *BTreeNode
	t    int
}

// NewBTree creates an empty B tree
func NewBTree(t int) *BTree {
	return &BTree{root: &BTreeNode{leaf: true}, t: t}
}

// Search checks whether key exists
func (bt *BTree) Search(key int) bool {
	n := bt.root
	for {
		i := 0
		for i < len(n.keys) && key > n.keys[i] {
			i++
		}
		if i < len(n.keys) && key == n.keys[i] {
			return true
		}
		if n.leaf {
			return false
		}
		n = n.children[i]
	}
}

// splitChild splits x's i-th full child into two
func (bt *BTree) splitChild(x *BTreeNode, i int) {
	t := bt.t
	y := x.children[i]
	z := &BTreeNode{leaf: y.leaf}
	mid := y.keys[t-1]
	z.keys = append(z.keys, y.keys[t:]...)
	y.keys = y.keys[:t-1]
	if !y.leaf {
		z.children = append(z.children, y.children[t:]...)
		y.children = y.children[:t]
	}
	x.children = append(x.children, nil)
	copy(x.children[i+2:], x.children[i+1:])
	x.children[i+1] = z
	x.keys = append(x.keys, 0)
	copy(x.keys[i+1:], x.keys[i:])
	x.keys[i] = mid
}

// Insert inserts key
func (bt *BTree) Insert(key int) {
	if len(bt.root.keys) == 2*bt.t-1 {
		s := &BTreeNode{leaf: false, children: []*BTreeNode{bt.root}}
		bt.root = s
		bt.splitChild(s, 0)
		bt.insertNonFull(s, key)
	} else {
		bt.insertNonFull(bt.root, key)
	}
}

func (bt *BTree) insertNonFull(x *BTreeNode, key int) {
	i := len(x.keys) - 1
	if x.leaf {
		x.keys = append(x.keys, 0)
		for i >= 0 && key < x.keys[i] {
			x.keys[i+1] = x.keys[i]
			i--
		}
		x.keys[i+1] = key
		return
	}
	for i >= 0 && key < x.keys[i] {
		i--
	}
	i++
	if len(x.children[i].keys) == 2*bt.t-1 {
		bt.splitChild(x, i)
		if key > x.keys[i] {
			i++
		}
	}
	bt.insertNonFull(x.children[i], key)
}

// Traverse in-order traversal, yielding an ascending sequence
func (bt *BTree) Traverse() []int {
	var out []int
	var walk func(n *BTreeNode)
	walk = func(n *BTreeNode) {
		for i := 0; i < len(n.keys); i++ {
			if !n.leaf {
				walk(n.children[i])
			}
			out = append(out, n.keys[i])
		}
		if !n.leaf {
			walk(n.children[len(n.keys)])
		}
	}
	walk(bt.root)
	return out
}

func main() {
	bt := NewBTree(3)
	for _, k := range []int{10, 20, 5, 6, 12, 30, 7, 17, 3, 25} {
		bt.Insert(k)
	}
	fmt.Println("In-order traversal:", bt.Traverse())
	fmt.Println("Search 12:", bt.Search(12))
	fmt.Println("Search 15:", bt.Search(15))
}
```

Output:

```text
In-order traversal: [3 5 6 7 10 12 17 20 25 30]
Search 12: true
Search 15: false
```

### Complexity Analysis

Let $n$ be the total number of keys and $t$ the minimum degree; the height is $h \le \log_t \frac{n+1}{2}$:

- **Search / insert**: $O(\log_t n)$ node accesses; within a node, locating the position in a sorted array is $O(t)$.
- **Space**: $O(n)$.
- **I/O advantage**: the height is far smaller than for a binary tree; for example with $t=100$, a million-scale dataset has a height of only about 3 levels.

### Summary

A B tree combines "many keys per node" with "all leaves on the same level", trading pre-splitting for a balanced shape that never degrades. The split-and-promote-on-insert mechanism is shared by B+ trees and B* trees as well.

## References

- [B Tree · Wikipedia](https://en.wikipedia.org/wiki/B-tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [B+Tree](/algo/tree/B+Tree.md)
- [BinaryHeap](/algo/tree/BinaryHeap.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [B+Tree](/algo/tree/B+Tree.md)
- [BinaryHeap](/algo/tree/BinaryHeap.md)
