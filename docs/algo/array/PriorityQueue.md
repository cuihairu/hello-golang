# Priority Queue
In Go, a priority queue is a special kind of queue in which every element has a priority, and elements dequeue in order of that priority. The common implementation of a priority queue is based on a heap data structure, and in particular a binary heap. Go's standard library `container/heap` package provides support for priority queues.

### Basic Concepts of a Priority Queue

1. **Priority queue**:
   - **Insert operation**: insert an element into the queue while keeping the queue's priority order.
   - **Delete operation**: remove the element with the highest priority (usually the smallest or largest value).

2. **Heap**:
   - **Max-heap**: a heap whose top element is the largest of all elements.
   - **Min-heap**: a heap whose top element is the smallest of all elements.
   - In Go, the `container/heap` package implements a min-heap (that is, the top of the heap is the minimum).

### Implementing a Priority Queue in Go

Go's `container/heap` package provides a heap interface on top of which you can implement your own priority queue. The work splits into two steps:

1. **Define a priority queue type**:
   You need to implement the `heap.Interface`, which includes the `Len`, `Less`, `Swap`, `Push`, and `Pop` methods.

2. **Implement the priority queue**:
   Implement the methods of the `heap.Interface` and use the functionality provided by the `heap` package to manage the priority queue.


### Array as the Underlying Data Structure

1. **Array basics**:
    
    - In Go's `container/heap` package, a priority queue is usually implemented on top of an array. This array represents a heap data structure, where each node of the heap is stored at one position in the array.
2. **Heap properties**:
    
    - A heap is a complete binary tree that can be represented efficiently with an array. For an element in the heap, if its index in the array is `i`, then:
        - the **left child** has index `2*i + 1`
        - the **right child** has index `2*i + 2`
        - the **parent** has index `(i - 1) / 2`
    - With these three relations, any index directly yields its parent and children positions, with no traversal needed.

### Implementation Details

1. **Data storage**:
    
    - In a priority queue implementation, the underlying data is stored in a slice (`slice`), which behaves much like an array but can grow and shrink dynamically.
2. **Insert operation**:
    
    - When inserting a new element, it is appended to the end of the array and then "bubbled up" to preserve the heap property.
3. **Delete operation**:
    
    - A delete usually removes the root element, moves the last element of the heap to the top, and then "sinks" it down to restore the heap property.

### Example Code

Below is a simple priority queue example showing how to implement one in Go using the `container/heap` package:

```go
package main

import (
    "container/heap"
    "fmt"
)

// IntHeap implements the heap.Interface interface
type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] < h[j] } // min-heap
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *IntHeap) Push(x interface{}) {
    *h = append(*h, x.(int))
}

func (h *IntHeap) Pop() interface{} {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}

func main() {
    // create an IntHeap instance
    h := &IntHeap{2, 1, 5}
    heap.Init(h)

    // insert an element
    heap.Push(h, 3)
    fmt.Printf("Minimum: %d\n", (*h)[0])

    // remove elements
    for h.Len() > 0 {
        fmt.Printf("%d ", heap.Pop(h))
    }
}
```

### Code Walkthrough

1. **Defining the priority queue**: `IntHeap` implements the `heap.Interface` and is an integer min-heap. `Len` and `Swap` are just routine slice operations; the priority rule lives in `Less`, where `h[i] < h[j]` means the smallest sits at the top; `Push` appends the element to the end of the slice, and `Pop` takes the last element and shrinks.

2. **Using the priority queue**:
   - Create an `IntHeap` instance and initialize it.
   - Use `heap.Push` to insert a new element.
   - Use `heap.Pop` to remove and return the highest-priority element.

### Application Scenarios

1. **Task scheduling**:
   - Scheduling tasks with different priorities so that high-priority tasks run first.

2. **A* search algorithm**:
   - Used in pathfinding algorithms to select the optimal path.

3. **Real-time data processing**:
   - Handling and maintaining priority information in data streams.

### Complexity

`heap.Push` and `heap.Pop` are both O(log n), costing one bubble-up or sink-down. Reading the head (the element at index 0) is O(1). `heap.Init` arranges n elements into a heap in O(n). The underlying slice grows on demand, and `heap.Fix` restores the heap order after an element has been modified, also O(log n).

### Summary

The standard library does not provide a ready-made priority queue type: `container/heap` only offers the interface and a few operation functions, and the queue itself has to be defined by you. Implement the five methods of `heap.Interface`, then drive it with `heap.Init`, `heap.Push`, and `heap.Pop`. Putting a less-than in `Less` gives you a min-heap; switch it to greater-than and you get a max-heap.

## References

- [Priority queue · Wikipedia](https://en.wikipedia.org/wiki/Priority_queue)
- [container/heap standard library](https://pkg.go.dev/container/heap)


## Sibling pages

- [DynamicArray](/algo/array/DynamicArray.md)
- [Array](/algo/array/Array.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)
- [MultidimensionalArray](/algo/array/MultidimensionalArray.md)
- [SparseArray](/algo/array/SparseArray.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [MultidimensionalArray](/algo/array/MultidimensionalArray.md)
- [SparseArray](/algo/array/SparseArray.md)
