### Bubble Sort

Bubble sort repeatedly traverses the list, step by step "bubbling" the largest (or smallest) element to the end. Time complexity $O(n^2)$, mostly used for teaching and small-scale data.

#### 1. The basics of bubble sort

The process of bubble sort goes as follows:

1. **Traverse and compare**:
   - Starting from the beginning of the list, compare adjacent elements in sequence.
   - If the earlier element is greater than the later one, swap them.

2. **Adjust the sort range**:
   - After each pass, the largest element is placed at the end of the list.
   - As sorting proceeds, the unsorted range gradually shrinks.

3. **Early exit optimization**:
   - If a pass produces no swaps, the list is already sorted, so you can exit early and avoid unnecessary passes.

#### 2. Algorithm steps of bubble sort

1. **Outer loop**: from the start of the list to the second-to-last element.
   - **Inner loop**: from the start of the list to the i-th element from the end, comparing adjacent elements.
   - If the earlier element is greater than the later one, swap them.

2. **Early exit**:
   - If no swaps occur in the inner loop, the list is already sorted, so you can exit the outer loop.

#### 3. Time and space complexity of bubble sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$, when the array is fully reversed, up to $n(n-1)/2$ comparisons and swaps are needed.
  - **Best case**: $O(n)$, when the array is already sorted, only one pass with no swaps is required.
  - **Average case**: $O(n^2)$, sorting a randomly ordered array has an average time complexity of $O(n^2)$.

- **Space complexity**: $O(1)$, bubble sort is in-place and only uses an extra variable for swapping.

#### 4. Code example of bubble sort

```go
package main

import "fmt"

// BubbleSort sorts an int slice using bubble sort
func BubbleSort(arr []int) {
    n := len(arr)
    for i := 0; i < n-1; i++ {
        swapped := false
        for j := 0; j < n-i-1; j++ {
            if arr[j] > arr[j+1] {
                // swap elements
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = true
            }
        }
        // no swaps means already sorted, exit early
        if !swapped {
            break
        }
    }
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    BubbleSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of bubble sort

**Pros**:
- Simple to implement, easy to understand and write.
- Suitable for small datasets.

**Cons**:
- Inefficient for large datasets, time complexity is $O(n^2)$.
- Not suitable for performance-sensitive scenarios.

### Summary

Bubble sort keeps swapping adjacent out-of-order pairs, gradually moving elements into their correct positions. The code is only a dozen lines, easy to read; once the data grows, $O(n^2)$ can no longer hold up.

## References

- [Bubble Sort · Wikipedia](https://en.wikipedia.org/wiki/Bubble_sort)

## Sibling pages

- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [CountingSort](/algo/sort/CountingSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [CountingSort](/algo/sort/CountingSort.md)
- [HeapSort](/algo/sort/HeapSort.md)
- [InsertionSort](/algo/sort/InsertionSort.md)
- [MergeSort](/algo/sort/MergeSort.md)
- [QuickSort](/algo/sort/QuickSort.md)
- [RadixSort](/algo/sort/RadixSort.md)
- [SelectionSort](/algo/sort/SelectionSort.md)
- [ShellSort](/algo/sort/ShellSort.md)
- [Sort](/algo/sort/Sort.md)
- [StableSort](/algo/sort/StableSort.md)
- [TimSort](/algo/sort/TimSort.md)
