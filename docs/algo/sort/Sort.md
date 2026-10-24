# Sorting
Same goal — sorting — but different algorithms make very different trade-offs between time, space and stability. Below are the complexity and stability of 6 common sorting algorithms, followed by a comparison table.

### 1. Bubble Sort

- **Time complexity**:
  - Worst case: O(n²)
  - Average case: O(n²)
  - Best case: O(n) (when the array is already sorted)
- **Space complexity**: O(1) (in-place sort)
- **Stability**: stable
- **Description**: Bubble sort is a simple sorting algorithm that repeatedly walks through the elements to be sorted, compares adjacent elements and swaps any that are out of order, so that larger elements "bubble" to the end of the array. Because its time complexity is high, it is usually not suitable for sorting large amounts of data.

### 2. Selection Sort

- **Time complexity**:
  - Worst case: O(n²)
  - Average case: O(n²)
  - Best case: O(n²)
- **Space complexity**: O(1) (in-place sort)
- **Stability**: unstable
- **Description**: Selection sort keeps choosing the smallest (or largest) element of the unsorted part and moves it to the end of the sorted part. Simple to implement, but it gets slow fast once the data gets large.

### 3. Insertion Sort

- **Time complexity**:
  - Worst case: O(n²)
  - Average case: O(n²)
  - Best case: O(n) (when the array is already sorted)
- **Space complexity**: O(1) (in-place sort)
- **Stability**: stable
- **Description**: Insertion sort builds a sorted subsequence and inserts each new element into its correct position within that subsequence. Suitable for small amounts of data and for partially sorted data.

### 4. Quick Sort

- **Time complexity**:
  - Worst case: O(n²) (when the chosen pivot causes an extreme imbalance)
  - Average case: O(n log n)
  - Best case: O(n log n)
- **Space complexity**: O(log n) (recursive stack space)
- **Stability**: unstable
- **Description**: Quick sort uses a divide-and-conquer strategy: it picks a pivot element to split the array into two subarrays and recursively sorts the subarrays. It performs well on average, but degrades to O(n²) when the pivot is a poor choice.

### 5. Merge Sort

- **Time complexity**:
  - Worst case: O(n log n)
  - Average case: O(n log n)
  - Best case: O(n log n)
- **Space complexity**: O(n) (needs extra space to store the temporary arrays)
- **Stability**: stable
- **Description**: Merge sort uses a divide-and-conquer strategy to split the array into two halves, sorts each half, then merges the sorted halves. All three cases are O(n log n); the cost is O(n) extra space for the merge.

### 6. Heap Sort

- **Time complexity**:
  - Worst case: O(n log n)
  - Average case: O(n log n)
  - Best case: O(n log n)
- **Space complexity**: O(1) (in-place sort)
- **Stability**: unstable
- **Description**: Heap sort is based on the heap data structure: it builds the array to be sorted into a max-heap (or min-heap), then moves the heap top element to the end of the array step by step. Suitable for scenarios that need to sort data in place.

### Comparison of the algorithms

| Sorting algorithm | Time complexity (worst) | Time complexity (average) | Time complexity (best) | Space complexity | Stability |
|-------------------|-------------------------|---------------------------|------------------------|------------------|-----------|
| Bubble sort       | O(n²)                   | O(n²)                     | O(n)                   | O(1)             | stable    |
| Selection sort    | O(n²)                   | O(n²)                     | O(n²)                  | O(1)             | unstable  |
| Insertion sort    | O(n²)                   | O(n²)                     | O(n)                   | O(1)             | stable    |
| Quick sort        | O(n²)                   | O(n log n)                | O(n log n)             | O(log n)         | unstable  |
| Merge sort        | O(n log n)              | O(n log n)                | O(n log n)             | O(n)             | stable    |
| Heap sort         | O(n log n)              | O(n log n)                | O(n log n)             | O(1)             | unstable  |

There is no single best choice across all scenarios. When the data is mostly sorted already, insertion sort is close to O(n); if you want stability and do not mind extra memory, use merge sort; if memory is tight, pick an in-place algorithm like heap sort.

## References

- [Sorting algorithms · Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm)
- [sort standard library](https://pkg.go.dev/sort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [ShellSort](/algo/sort/ShellSort.md)
- [StableSort](/algo/sort/StableSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ShellSort](/algo/sort/ShellSort.md)
- [StableSort](/algo/sort/StableSort.md)
