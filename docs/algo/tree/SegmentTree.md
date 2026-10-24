# Segment Tree

A segment tree is a binary tree that recursively bisects the intervals of an array: the root node represents the whole array, each internal node splits its interval in the middle, and leaf nodes represent single elements. Each node stores some aggregate information about its interval (sum, minimum/maximum, etc.), so that "range query plus range/point update" are both $O(\log n)$.

### Structural Characteristics

1. **Interval bisection**: each node corresponds to an interval `[l, r]`, with left child `[l, mid]` and right child `[mid+1, r]`.
2. **Array storage**: nodes are numbered the way a heap is (root is 1, children are `2*node` and `2*node+1`), so $4n$ space is enough to hold them all.
3. **Information bubbling up**: after a child node is updated, the parent node is recomputed by aggregating its two children.

### Algorithm Steps (Range Sum)

1. **Build**: recurse down to the leaves and store the original values; on the way back, `tree[node] = tree[left] + tree[right]`.
2. **Point update**: descend along the path to the leaf and change the value, then update the nodes along the way on the way back.
3. **Range query**: if the current node's interval is fully contained, return directly; otherwise recurse into the left and right sides as appropriate and merge the results.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// SegmentTree segment tree (range sum, single point update)
type SegmentTree struct {
	n    int
	tree []int
}

// NewSegmentTree builds a segment tree from an array
func NewSegmentTree(arr []int) *SegmentTree {
	st := &SegmentTree{n: len(arr), tree: make([]int, 4*len(arr))}
	var build func(node, l, r int)
	build = func(node, l, r int) {
		if l == r {
			st.tree[node] = arr[l]
			return
		}
		mid := (l + r) / 2
		build(node*2, l, mid)
		build(node*2+1, mid+1, r)
		st.tree[node] = st.tree[node*2] + st.tree[node*2+1]
	}
	build(1, 0, len(arr)-1)
	return st
}

// Update changes the value at index i to val
func (st *SegmentTree) Update(i, val int) {
	var rec func(node, l, r int)
	rec = func(node, l, r int) {
		if l == r {
			st.tree[node] = val
			return
		}
		mid := (l + r) / 2
		if i <= mid {
			rec(node*2, l, mid)
		} else {
			rec(node*2+1, mid+1, r)
		}
		st.tree[node] = st.tree[node*2] + st.tree[node*2+1]
	}
	rec(1, 0, st.n-1)
}

// Query computes the range sum [ql, qr]
func (st *SegmentTree) Query(ql, qr int) int {
	var rec func(node, l, r int) int
	rec = func(node, l, r int) int {
		if ql <= l && r <= qr {
			return st.tree[node]
		}
		mid := (l + r) / 2
		sum := 0
		if ql <= mid {
			sum += rec(node*2, l, mid)
		}
		if qr > mid {
			sum += rec(node*2+1, mid+1, r)
		}
		return sum
	}
	return rec(1, 0, st.n-1)
}

func main() {
	arr := []int{1, 3, 5, 7, 9}
	st := NewSegmentTree(arr)

	fmt.Println("Range sum [1..3]:", st.Query(1, 3)) // 3+5+7 = 15
	st.Update(2, 10)                                 // a[2] = 10
	fmt.Println("After update [1..3]:", st.Query(1, 3)) // 3+10+7 = 20
	fmt.Println("Total array sum:", st.Query(0, 4))    // 1+3+10+7+9 = 30
}
```

Output:

```text
Range sum [1..3]: 15
After update [1..3]: 20
Total array sum: 30
```

### Complexity Analysis

- **Build**: $O(n)$; there are $n$ leaf-level nodes and each level above has half as many, for a total of $2n-1$.
- **Point update / range query**: $O(\log n)$, walking only one or two branches each time.
- **Space**: $O(4n)$.
- With lazy propagation added, range updates can also be done in $O(\log n)$; see the "implicit segment tree" chapter for a demonstration of tagging.

### Application Scenarios

- Queries over mergeable interval information such as range sum / min-max / XOR.
- Variants like sweep-line rectangle area union, interval coloring, interval historical extremes.

### Summary

A segment tree turns an "array" into a "recursively bisectable structure"; any interval information that satisfies the associative law can be attached to a node. Its template is longer than a Fenwick tree's, but it covers more complex scenarios such as range updates and maintaining multiple pieces of information.

## References

- [Segment Tree · Wikipedia](https://en.wikipedia.org/wiki/Segment_tree)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [Tree](/algo/tree/Tree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Tree](/algo/tree/Tree.md)
