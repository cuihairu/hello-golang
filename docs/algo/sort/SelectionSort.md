### Selection Sort

Each round, selection sort picks the smallest element from the part still to be sorted and swaps it with the first slot of that part, so the sorted prefix grows by one. The implementation is only a few lines; the price is a time complexity fixed at $O(n^2)$, which gets slow once the data grows.

#### 1. The basics of selection sort

1. **Select the smallest element**:
   - Pick the smallest element from the part of the list still to be sorted.
   - Swap that smallest element with the first element of the current unsorted range.

2. **Shrink the sorting range**:
   - The sorted portion extends from the start of the list while the range of unsorted elements shrinks.
   - Repeat the steps above until all elements are sorted.

#### 2. Algorithm steps of selection sort

1. **Outer loop**: from the start of the list to the second-to-last element.
   - Select the smallest element in the unsorted part.

2. **Inner loop**: from the current start position to the end of the list, find the index of the smallest element.

3. **Swap**:
   - Swap the smallest element found with the element at the current start position.

4. **Repeat**:
   - Keep repeating the steps above on the remaining unsorted part until the whole list is sorted.

#### 3. Time and space complexity of selection sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$, whatever the initial state of the data, every selection of the smallest element requires scanning the unsorted part.
  - **Best case**: $O(n^2)$, even when the array is already sorted, the full scans are still needed.
  - **Average case**: $O(n^2)$, sorting a randomly ordered array averages to $O(n^2)$.

- **Space complexity**:
  - **Space complexity**: $O(1)$, selection sort is an in-place algorithm and needs no extra storage beyond the variable used for swapping.

#### 4. Code example of selection sort

```go
package main

import "fmt"

// SelectionSort selection sorts a slice of integers
func SelectionSort(arr []int) {
    n := len(arr)
    for i := 0; i < n-1; i++ {
        // assume the current element is the smallest
        minIndex := i
        // find the smallest element in the unsorted part
        for j := i + 1; j < n; j++ {
            if arr[j] < arr[minIndex] {
                minIndex = j
            }
        }
        // swap the smallest element with the current element
        if minIndex != i {
            arr[i], arr[minIndex] = arr[minIndex], arr[i]
        }
    }
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    SelectionSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of selection sort

**Pros**:
- Simple to implement and easy to understand and write.
- Works well on small datasets.

**Cons**:
- Time complexity is $O(n^2)$, so it is inefficient on large datasets.
- Not a stable sorting algorithm (elements with equal values may change their relative positions).

### Summary

Selection sort has three properties you can count on: the time complexity is a fixed $O(n^2)$, independent of the initial order; the space is $O(1)$, using only the variable for swapping; and the implementation is short, so reading the code shows at a glance how the sort proceeds. Large datasets do not suit it; the short implementation, on the other hand, is handy for following the sorting process step by step.

## References

- [Selection sort · Wikipedia](https://en.wikipedia.org/wiki/Selection_sort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [RadixSort](/algo/sort/RadixSort.md)
- [ShellSort](/algo/sort/ShellSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [RadixSort](/algo/sort/RadixSort.md)
- [ShellSort](/algo/sort/ShellSort.md)
