# Fenwick Tree

A Fenwick tree (Fenwick Tree, Binary Indexed Tree) maintains prefix sums with a compact array and supports **single-point updates** and **range queries**, both in $O(\log n)$. Peter Fenwick introduced it in 1994; the code is far shorter than a segment tree's, making it the implementation of choice for prefix-sum problems.

### Core Idea

1. **lowbit**: `lowbit(x) = x & -x` picks out the lowest set bit in binary; for example `lowbit(6) = 2`.
2. **Tree structure**: the element at index `i` is responsible for the sum over the interval `(i - lowbit(i), i]`, and its parent in the "tree" is `i + lowbit(i)`.
3. **Indexing convention**: element indices start at 1 (index 0 has no lowbit); the code maps the original array with `i+1`.

### Algorithm Steps

1. **Update(i, delta)**: starting at `i`, walk upward with `i += lowbit(i)`, adding delta into every node that covers this position.
2. **Query(i)**: starting at `i`, walk downward with `i -= lowbit(i)`, accumulating the sum, to get the prefix sum `a[1..i]`.
3. **Range sum [l, r]**: `Query(r) - Query(l-1)`.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// FenwickTree is a Fenwick tree (binary indexed tree)
type FenwickTree struct {
	n   int
	bit []int
}

// NewFenwickTree creates a Fenwick tree holding n elements
func NewFenwickTree(n int) *FenwickTree {
	return &FenwickTree{n: n, bit: make([]int, n+1)}
}

// lowbit returns the lowest set bit
func lowbit(x int) int { return x & -x }

// Update adds delta to the element at index i (1-based)
func (f *FenwickTree) Update(i, delta int) {
	for i <= f.n {
		f.bit[i] += delta
		i += lowbit(i)
	}
}

// Query returns the prefix sum [1, i]
func (f *FenwickTree) Query(i int) int {
	sum := 0
	for i > 0 {
		sum += f.bit[i]
		i -= lowbit(i)
	}
	return sum
}

// RangeQuery returns the range sum [l, r] (1-based indices)
func (f *FenwickTree) RangeQuery(l, r int) int {
	return f.Query(r) - f.Query(l-1)
}

func main() {
	arr := []int{1, 3, 5, 7, 9, 11}
	f := NewFenwickTree(len(arr))
	for i, v := range arr {
		f.Update(i+1, v)
	}

	fmt.Println("prefix sum[1..3]:", f.Query(3))        // 1+3+5 = 9
	fmt.Println("range sum[2..5]:", f.RangeQuery(2, 5))   // 3+5+7+9 = 24

	f.Update(3, 2) // 3rd element +2
	fmt.Println("range sum[2..5] after update:", f.RangeQuery(2, 5))
	fmt.Println("sum of whole array:", f.Query(len(arr)))
}
```

Output:

```text
prefix sum[1..3]: 9
range sum[2..5]: 24
range sum[2..5] after update: 26
sum of whole array: 38
```

### Complexity Analysis

- **Single-point update**: $O(\log n)$, at most $\log n$ levels walked up the tree.
- **Prefix/range query**: $O(\log n)$.
- **Space**: $O(n)$, just one array of length $n+1$.
- **Limitation**: it only handles range sums of the "single-point update + prefix query" kind; a range update needs the difference trick to reduce it to point updates plus prefix queries, or you switch to a segment tree.

### Use Cases

- Counting inversions, and finding the k-th smallest in a range (paired with coordinate compression of the value domain).
- Two-dimensional prefix sums (2D Fenwick tree), and DFS-order maintenance for tree problems.

### Summary

A Fenwick tree binds "increments of prefix sums" to "the binary structure of indices", reaching segment-tree-level $O(\log n)$ complexity with `lowbit` in only a dozen or so lines of code. For small-scale range statistics it is enough, and far less effort than a segment tree.

## References

- [Binary indexed tree · Wikipedia](https://en.wikipedia.org/wiki/Fenwick_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [CompleteBinaryTree](/algo/tree/CompleteBinaryTree.md)
- [FullBinaryTree](/algo/tree/FullBinaryTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [CompleteBinaryTree](/algo/tree/CompleteBinaryTree.md)
- [FullBinaryTree](/algo/tree/FullBinaryTree.md)
