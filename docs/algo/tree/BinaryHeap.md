# Binary Heap

A binary heap is the direct product of a complete binary tree and the heap-order property: because it is a complete binary tree, it can be laid out in an array as-is, and parent-child relations are computed from indices alone — the parent of index `i` is `(i-1)/2`, and its children are `2i+1` and `2i+2`. This page demonstrates heap construction and heap sort using a max heap.

### Array Representation

1. **Parent**: `(i-1)/2`.
2. **Left child**: `2i+1`, **right child**: `2i+2`.
3. **Leaf nodes**: indices from $\lfloor n/2 \rfloor$ to $n-1$; they have no children and need no sinking.

### Algorithm Steps (Heap Sort)

1. **Build heap**: starting from the last non-leaf node $\lfloor n/2 \rfloor - 1$, sink each node in reverse order, bottom-up, to produce a max heap in $O(n)$.
2. **Sort**: swap the root (the maximum) with the last element, shrink the heap by one, then sink the new root; repeat $n-1$ times.
3. The resulting array is the ascending sequence.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// siftDown sinks the element at index i down to its correct position within arr[0..n)
func siftDown(arr []int, n, i int) {
	for {
		left, right := 2*i+1, 2*i+2
		largest := i
		if left < n && arr[left] > arr[largest] {
			largest = left
		}
		if right < n && arr[right] > arr[largest] {
			largest = right
		}
		if largest == i {
			return
		}
		arr[i], arr[largest] = arr[largest], arr[i]
		i = largest
	}
}

// heapSort in-place heap sort (ascending)
func heapSort(arr []int) {
	n := len(arr)
	// build a max heap bottom-up, O(n)
	for i := n/2 - 1; i >= 0; i-- {
		siftDown(arr, n, i)
	}
	// each time move the heap's max value to the end, then repair the heap
	for end := n - 1; end > 0; end-- {
		arr[0], arr[end] = arr[end], arr[0]
		siftDown(arr, end, 0)
	}
}

func main() {
	arr := []int{9, 4, 7, 1, 8, 2, 6}
	fmt.Println("Original array:", arr)
	heapSort(arr)
	fmt.Println("Sorted array:", arr)

	empty := []int{}
	heapSort(empty)
	fmt.Println("Empty array:", empty)
}
```

Output:

```text
Original array: [9 4 7 1 8 2 6]
Sorted array: [1 2 4 6 7 8 9]
Empty array: []
```

### Complexity Analysis

- **Build heap**: $O(n)$. The $h$-th level has at most $n/2^{h+1}$ nodes, each sinking $h$ levels, and summing gives $\sum h \cdot n/2^{h+1} = O(n)$.
- **Sort**: $O(n \log n)$, with $n-1$ swaps each followed by an $O(\log n)$ sift.
- **Space**: $O(1)$, in-place; **unstable** (long-distance swaps scramble the order of equal elements).

### Summary

The value of a binary heap lies in "structure + indices": the shape of a complete binary tree turns every pointer into arithmetic, so heap sort can run in place. Its instability and poorer cache locality are the drawbacks compared with quicksort, but the $O(n)$ heap build and the $O(\log n)$ dynamic extreme-value maintenance are things quicksort cannot offer.

## References

- [Binary Heap · Wikipedia](https://en.wikipedia.org/wiki/Binary_heap)
- [container/heap standard library](https://pkg.go.dev/container/heap)


## Sibling pages

- [Heap](/algo/tree/Heap.md)
- [MinimumSpanningTree](/algo/tree/MinimumSpanningTree.md)
- [RedBlackTree](/algo/tree/RedBlackTree.md)
- [BTree](/algo/tree/BTree.md)
- [BinarySearchTree](/algo/tree/BinarySearchTree.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BTree](/algo/tree/BTree.md)
- [BinarySearchTree](/algo/tree/BinarySearchTree.md)
