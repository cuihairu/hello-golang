# Minimum Spanning Tree

A minimum spanning tree (MST) picks out a tree from a connected undirected weighted graph that includes all $n$ vertices and minimizes the total edge weight. Kruskal's algorithm builds it with a greedy strategy — "sort edges by weight ascending, pick an edge if it doesn't form a cycle" — and uses a disjoint set union (DSU) to detect cycles, for a time complexity of $O(E \log E)$.

### Kruskal's Algorithm Steps

1. Sort all edges by weight in ascending order.
2. Examine each edge `(u, v)` in turn: if `u` and `v` are not yet connected (different roots in the DSU), add it to the spanning tree and merge the two sets; otherwise discard it (it would form a cycle).
3. Stop when $n-1$ edges are chosen or the edges are exhausted. The chosen edges form the minimum spanning tree.

### Code Example (Go Implementation)

```go
package main

import (
	"fmt"
	"sort"
)

// Edge undirected weighted edge
type Edge struct {
	u, v, w int
}

// DSU disjoint set union (with path compression)
type DSU struct {
	parent []int
}

func NewDSU(n int) *DSU {
	p := make([]int, n)
	for i := range p {
		p[i] = i
	}
	return &DSU{parent: p}
}

func (d *DSU) Find(x int) int {
	for d.parent[x] != x {
		d.parent[x] = d.parent[d.parent[x]] // path compression
		x = d.parent[x]
	}
	return x
}

// Union merges two sets; returns false if they are already in the same set
func (d *DSU) Union(a, b int) bool {
	ra, rb := d.Find(a), d.Find(b)
	if ra == rb {
		return false
	}
	d.parent[ra] = rb
	return true
}

// kruskal finds the minimum spanning tree, returning the chosen edges and total weight
func kruskal(n int, edges []Edge) ([]Edge, int) {
	sorted := append([]Edge(nil), edges...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i].w < sorted[j].w })

	dsu := NewDSU(n)
	var mst []Edge
	total := 0
	for _, e := range sorted {
		if dsu.Union(e.u, e.v) {
			mst = append(mst, e)
			total += e.w
			if len(mst) == n-1 {
				break
			}
		}
	}
	return mst, total
}

func main() {
	edges := []Edge{
		{0, 1, 4}, {0, 2, 1}, {2, 1, 2}, {1, 3, 5}, {2, 3, 8},
	}
	mst, total := kruskal(4, edges)
	fmt.Println("MST edges:")
	for _, e := range mst {
		fmt.Printf("  %d - %d (w=%d)\n", e.u, e.v, e.w)
	}
	fmt.Println("Total weight:", total)
}
```

Output:

```text
MST edges:
  0 - 2 (w=1)
  2 - 1 (w=2)
  1 - 3 (w=5)
Total weight: 8
```

### Complexity Analysis

- **Sorting**: $O(E \log E)$, dominates the whole algorithm.
- **DSU operations**: amortized approximately $O(1)$ (path compression + union by rank).
- **Space**: $O(V + E)$.

### Application Scenarios

- Problems like network cabling, power grids, and pipeline laying — "connect all nodes with minimum total cost."
- Clustering analysis (delete the longest few edges to get clusters); the foundational structure for approximation algorithms.

### Summary

The correctness of the greedy approach for MST is guaranteed by the "cut property": at any point, the minimum edge crossing the two sets (chosen / not chosen) must belong to some minimum spanning tree. Most of Kruskal's implementation lives in the DSU: cycle detection relies on `Union` returning `false`, edge selection relies on it merging two sets, and it stops once $n-1$ edges are chosen.

## References

- [Minimum Spanning Tree · Wikipedia](https://en.wikipedia.org/wiki/Minimum_spanning_tree)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Graph](/algo/Graph.md)
- [AVLTree](/algo/tree/AVLTree.md)
- [B+Tree](/algo/tree/B+Tree.md)
- [BTree](/algo/tree/BTree.md)
- [BinaryHeap](/algo/tree/BinaryHeap.md)
- [BinarySearchTree](/algo/tree/BinarySearchTree.md)
- [BinaryTree](/algo/tree/BinaryTree.md)
- [CompleteBinaryTree](/algo/tree/CompleteBinaryTree.md)
- [FenwickTree](/algo/tree/FenwickTree.md)
- [FullBinaryTree](/algo/tree/FullBinaryTree.md)
- [HuffmanTree](/algo/tree/HuffmanTree.md)
- [PrefixTree](/algo/tree/PrefixTree.md)
- [SegmentTree](/algo/tree/SegmentTree.md)
- [Tree](/algo/tree/Tree.md)
