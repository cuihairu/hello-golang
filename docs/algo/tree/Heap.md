# Heap

A heap is a complete binary tree that also satisfies the heap property: in a min-heap every node is less than or equal to its children, and in a max-heap every node is greater than or equal to its children. The top of the heap is therefore always the smallest (largest) element of the whole heap; insert, delete and read-top are all $O(\log n)$, so the heap is the standard implementation of a priority queue.

### Core Properties

1. **Structural property**: a complete binary tree, storable compactly in an array with no holes.
2. **Heap property**: it only constrains the ordering "parent versus child"; siblings are unordered, and the left and right subtrees are unordered with respect to each other.
3. **Basic operations**:
   - **Push**: append to the end, then **sift up** (compare and swap with the parent).
   - **Pop**: take out the top, move the last element to the top, then **sift down** (swap with the smaller/larger child).
   - **Peek**: read the top directly, $O(1)$.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// MinHeap is a min-heap
type MinHeap struct {
	data []int
}

// Push adds v to the heap and sifts it up
func (h *MinHeap) Push(v int) {
	h.data = append(h.data, v)
	h.up(len(h.data) - 1)
}

// Pop removes and returns the top (minimum)
func (h *MinHeap) Pop() (int, bool) {
	if len(h.data) == 0 {
		return 0, false
	}
	top := h.data[0]
	last := len(h.data) - 1
	h.data[0] = h.data[last]
	h.data = h.data[:last]
	if last > 0 {
		h.down(0)
	}
	return top, true
}

// Peek returns the top
func (h *MinHeap) Peek() (int, bool) {
	if len(h.data) == 0 {
		return 0, false
	}
	return h.data[0], true
}

// Len returns the number of elements in the heap
func (h *MinHeap) Len() int { return len(h.data) }

// up sifts the element at index i upward
func (h *MinHeap) up(i int) {
	for i > 0 {
		parent := (i - 1) / 2
		if h.data[i] >= h.data[parent] {
			break
		}
		h.data[i], h.data[parent] = h.data[parent], h.data[i]
		i = parent
	}
}

// down sifts the element at index i downward
func (h *MinHeap) down(i int) {
	n := len(h.data)
	for {
		left, right := 2*i+1, 2*i+2
		smallest := i
		if left < n && h.data[left] < h.data[smallest] {
			smallest = left
		}
		if right < n && h.data[right] < h.data[smallest] {
			smallest = right
		}
		if smallest == i {
			return
		}
		h.data[i], h.data[smallest] = h.data[smallest], h.data[i]
		i = smallest
	}
}

func main() {
	h := &MinHeap{}
	for _, v := range []int{5, 3, 8, 1, 9} {
		h.Push(v)
	}
	if v, ok := h.Peek(); ok {
		fmt.Println("peek:", v)
	}
	for h.Len() > 0 {
		v, _ := h.Pop()
		fmt.Println("pop:", v)
	}
}
```

Output:

```text
peek: 1
pop: 1
pop: 3
pop: 5
pop: 8
pop: 9
```

### Complexity Analysis

- **Push / Pop**: $O(\log n)$; the path length is the tree height.
- **Peek**: $O(1)$.
- **Heapify (bottom-up sifting down)**: $O(n)$, better than the $O(n \log n)$ of pushing one at a time.
- **Space**: $O(n)$.

### Use Cases

- Priority queues, task scheduling (the Go standard library provides `container/heap`).
- Heapsort, Top-K problems, multi-way merge, Dijkstra's shortest path.

### Summary

A heap uses two constraints — "complete binary tree + ordered parent/child" — to buy $O(1)$ read-top and $O(\log n)$ insert/delete, landing somewhere between "a completely unordered array" and "a completely ordered BST". All heap operations come down to just two moves: sifting up and sifting down.

## References

- [Heap (data structure) · Wikipedia](https://en.wikipedia.org/wiki/Heap_%28data_structure%29))
- [container/heap standard library](https://pkg.go.dev/container/heap)

## Sibling pages

- [HuffmanTree](/algo/tree/HuffmanTree.md)
- [PrefixTree](/algo/tree/PrefixTree.md)

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
