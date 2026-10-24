# B+ Tree

A B+ tree is a variant of the B tree and the de facto standard for database indexes: **all data lives in the leaf layer**, and internal nodes hold only the separator keys used for navigation. At the same time the leaf nodes are linked together by pointers into an **ordered linked list**, so a range scan becomes a sequential read along the list. MySQL InnoDB's primary key index is a B+ tree.

### Differences from a B Tree

1. **Data only in leaves**: internal nodes are just "signposts", so a node of the same size can hold more signposts and the tree is shorter.
2. **Leaves linked**: once you find the start of the range, just scan forward along the `next` pointers; no need to go back up.
3. **Every query reaches a leaf**: whether it hits or not, the search path length is the same.

### Implementation Notes

This page builds the tree with a **bulk load**: leaves are split by capacity and linked into a chain, and each higher level collapses upward using the "minimum key of the right child" as its separator key, until only one root remains. This is the fastest and least error-prone way to build a B+ tree, and it suits loading a large batch of already-sorted data all at once.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// bpNode B+ tree node: internal nodes use keys+children, leaves use keys+vals+next
type bpNode struct {
	leaf     bool
	keys     []int
	children []*bpNode
	vals     []string
	next     *bpNode
}

// leftmostKey finds the first key of the leftmost leaf of a subtree (i.e. the subtree's minimum key)
func leftmostKey(n *bpNode) int {
	for !n.leaf {
		n = n.children[0]
	}
	return n.keys[0]
}

// buildBPlusTree bulk load: keys must be ascending, maxKeys is the max keys per node
func buildBPlusTree(keys []int, vals []string, maxKeys int) *bpNode {
	// 1. split the leaf level and link the chain
	var leaves []*bpNode
	for i := 0; i < len(keys); i += maxKeys {
		j := i + maxKeys
		if j > len(keys) {
			j = len(keys)
		}
		leaves = append(leaves, &bpNode{
			leaf: true,
			keys: append([]int(nil), keys[i:j]...),
			vals: append([]string(nil), vals[i:j]...),
		})
	}
	for i := 0; i+1 < len(leaves); i++ {
		leaves[i].next = leaves[i+1]
	}
	// 2. build internal levels bottom-up
	level := leaves
	for len(level) > 1 {
		var next []*bpNode
		for i := 0; i < len(level); i += maxKeys {
			j := i + maxKeys
			if j > len(level) {
				j = len(level)
			}
			group := level[i:j]
			node := &bpNode{children: group}
			for _, c := range group[1:] {
				// separator key = the minimum key in the right subtree (first key of its leftmost leaf)
				node.keys = append(node.keys, leftmostKey(c))
			}
			next = append(next, node)
		}
		level = next
	}
	if len(level) == 0 {
		return nil
	}
	return level[0]
}

// Search finds the value for key
func Search(root *bpNode, key int) (string, bool) {
	n := root
	for n != nil && !n.leaf {
		i := 0
		for i < len(n.keys) && key >= n.keys[i] {
			i++
		}
		n = n.children[i]
	}
	if n == nil {
		return "", false
	}
	for i, k := range n.keys {
		if k == key {
			return n.vals[i], true
		}
	}
	return "", false
}

// RangeQuery returns all values whose key is in [lo, hi] (scanning the leaf chain)
func RangeQuery(root *bpNode, lo, hi int) []string {
	n := root
	for n != nil && !n.leaf {
		i := 0
		for i < len(n.keys) && lo >= n.keys[i] {
			i++
		}
		n = n.children[i]
	}
	var out []string
	for n != nil {
		for i, k := range n.keys {
			if k > hi {
				return out
			}
			if k >= lo {
				out = append(out, n.vals[i])
			}
		}
		n = n.next
	}
	return out
}

func main() {
	keys := []int{1, 3, 5, 7, 9, 11, 13, 15, 17, 19}
	vals := make([]string, len(keys))
	for i, k := range keys {
		vals[i] = fmt.Sprintf("row-%02d", k)
	}
	root := buildBPlusTree(keys, vals, 4)

	if v, ok := Search(root, 11); ok {
		fmt.Println("Search 11:", v)
	}
	_, ok := Search(root, 12)
	fmt.Println("Search 12:", ok)

	fmt.Println("Range [5,13]:", RangeQuery(root, 5, 13))
	fmt.Println("Range [14,19]:", RangeQuery(root, 14, 19))
	fmt.Println("Range [0,100]:", len(RangeQuery(root, 0, 100)), " rows")
}
```

Output:

```text
Search 11: row-11
Search 12: false
Range [5,13]: [row-05 row-07 row-09 row-11 row-13]
Range [14,19]: [row-15 row-17 row-19]
Range [0,100]: 10 rows
```

### Complexity Analysis

- **Search / locate range start**: $O(\log_m n)$ levels of navigation ($m$ is the node capacity).
- **Range query**: $O(\log_m n + k)$, where $k$ is the number of matches — read sequentially along the leaf chain.
- **Bulk load**: $O(n)$.
- **Space**: $O(n)$.

### Applications

- Database primary / secondary indexes, file systems (e.g. ext4's HTree).
- Any ordered store that needs both point lookup and range scan.

### Summary

A B+ tree pushes all the data down to the leaf layer, then links the leaves into a chain, turning range queries from level-by-level backtracking into a sequential scan. That is exactly why database indexes usually pick it over a B tree.

## References

- [B+ Tree · Wikipedia](https://en.wikipedia.org/wiki/B%2B_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [AVLTree](/algo/tree/AVLTree.md)
- [BTree](/algo/tree/BTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [AVLTree](/algo/tree/AVLTree.md)
- [BTree](/algo/tree/BTree.md)
