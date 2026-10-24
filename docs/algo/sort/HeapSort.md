Heap sort is a comparison-based sorting algorithm built on the heap data structure. A heap is a special kind of complete binary tree that satisfies one of the following properties:

- Max-heap: every node's value is greater than or equal to the values of its left and right children.
- Min-heap: every node's value is less than or equal to the values of its left and right children.

Use a max-heap for ascending order, and a min-heap for descending order.

### The basic steps of heap sort

Heap sort has two phases: building the heap and sorting.

#### 1. Build the heap

First build the array into a max-heap. Building the max-heap starts from the last non-leaf node and adjusts each node upward step by step, ensuring every subtree satisfies the max-heap property.

#### 2. Sort

Repeatedly remove the top element of the heap (the maximum), swap it with the last element of the heap, then adjust the heap to restore the max-heap property. Repeat this until every element has been placed.

### Implementation steps of heap sort

1. **Build the initial heap**: turn the unordered array into a max-heap.
2. **Adjust the heap**: swap the top element with the last element, shrink the heap size, and adjust the top to restore the heap property.
3. **Repeat step 2**: until the heap size is 1, at which point sorting is complete.

### Concrete implementation

#### Helper functions

- `heapify`: adjust the heap so it satisfies the max-heap property.
- `buildHeap`: build the initial heap.

```go
// heapify adjusts the heap so it satisfies the max-heap property
func heapify(arr []int, n, i int) {
    largest := i       // initialize largest as the current node
    l := 2*i + 1       // left child index
    r := 2*i + 2       // right child index

    // if the left child exists and is greater than the current node
    if l < n && arr[l] > arr[largest] {
        largest = l
    }

    // if the right child exists and is greater than the current node
    if r < n && arr[r] > arr[largest] {
        largest = r
    }

    // if largest is not the current node
    if largest != i {
        arr[i], arr[largest] = arr[largest], arr[i]  // swap
        heapify(arr, n, largest)                     // recursively adjust the subtree
    }
}

// buildHeap builds the initial max-heap
func buildHeap(arr []int, n int) {
    // start adjusting from the last non-leaf node
    for i := n/2 - 1; i >= 0; i-- {
        heapify(arr, n, i)
    }
}

// heapSort main function: build the heap, then move each heap top to the end
func heapSort(arr []int) {
    n := len(arr)

    // build the initial max-heap
    buildHeap(arr, n)

    // step by step swap the heap top with the last element and adjust the heap
    for i := n - 1; i > 0; i-- {
        arr[0], arr[i] = arr[i], arr[0]  // swap the heap top and the last element
        heapify(arr, i, 0)               // adjust the heap
    }
}
```

### Example

```go
package main

import "fmt"

// heapify function adjusts the heap
func heapify(arr []int, n, i int) {
    largest := i       // initialize largest as the current node
    l := 2*i + 1       // left child index
    r := 2*i + 2       // right child index

    // if the left child exists and is greater than the current node
    if l < n && arr[l] > arr[largest] {
        largest = l
    }

    // if the right child exists and is greater than the current node
    if r < n && arr[r] > arr[largest] {
        largest = r
    }

    // if largest is not the current node
    if largest != i {
        arr[i], arr[largest] = arr[largest], arr[i]  // swap
        heapify(arr, n, largest)                     // recursively adjust the subtree
    }
}

// buildHeap function builds the initial max-heap
func buildHeap(arr []int, n int) {
    // start adjusting from the last non-leaf node
    for i := n/2 - 1; i >= 0; i-- {
        heapify(arr, n, i)
    }
}

// heapSort function implements heap sort
func heapSort(arr []int) {
    n := len(arr)

    // build the initial max-heap
    buildHeap(arr, n)

    // step by step swap the heap top with the last element and adjust the heap
    for i := n - 1; i > 0; i-- {
        arr[0], arr[i] = arr[i], arr[0]  // swap the heap top and the last element
        heapify(arr, i, 0)               // adjust the heap
    }
}

func main() {
    arr := []int{12, 11, 13, 5, 6, 7}
    fmt.Println("Original array:", arr)

    heapSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

### Time and space complexity of heap sort

Heap sort has a time complexity of $O(n \log n)$, where $n$ is the number of elements in the array to sort. Specifically:

- Building the heap has a time complexity of $O(n)$.
- During sorting, each heap adjustment has a time complexity of $O(\log n)$, and $n-1$ adjustments are needed in total, so the sorting phase has a time complexity of $O(n \log n)$.

Heap sort has a space complexity of $O(1)$, because it needs only a constant amount of extra space for element swaps and heap adjustments.

Heap sort is an in-place sort with a steady time complexity of $O(n \log n)$, unaffected by the distribution of the input data.

## References

- [Heap Sort · Wikipedia](https://en.wikipedia.org/wiki/Heapsort)
- [container/heap standard library](https://pkg.go.dev/container/heap)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [CountingSort](/algo/sort/CountingSort.md)
- [InsertionSort](/algo/sort/InsertionSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [InsertionSort](/algo/sort/InsertionSort.md)
