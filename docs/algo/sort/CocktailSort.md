### Cocktail Sort

Cocktail sort, also known as bidirectional bubble sort or cocktail shaker sort, is a variant of bubble sort. It scans in both directions, sinking larger elements to the right end of the array in one pass and floating smaller elements to the left end, taking fewer rounds than unidirectional bubble sort.

#### 1. The basics of cocktail sort

The core idea of cocktail sort is:
1. **Bidirectional scan**: first scan from left to right, then from right to left; one round handles both large and small values at the same time, reducing the number of scan rounds.
2. **Adjacent swaps**: each scan relies on swapping adjacent elements, gradually putting the unsorted portion in order.

#### 2. Algorithm steps of cocktail sort

1. **Initialization**: set up two pointers, `left` and `right`, pointing to the beginning and the end of the array respectively.

2. **Forward scan (left to right)**:
   - Scan the array from left to right, moving larger elements to the right side (i.e. the end) of the array.
   - On each swap, update the position of the right pointer, because the already-sorted portion no longer needs to participate in sorting.

3. **Backward scan (right to left)**:
   - Scan the array from right to left, moving smaller elements to the left side (i.e. the beginning) of the array.
   - On each swap, update the position of the left pointer, because the already-sorted portion no longer needs to participate in sorting.

4. **Repeat the process**: keep repeating the forward and backward scans until the whole array is sorted.

#### 3. Time and space complexity of cocktail sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$, the same as bubble sort.
  - **Best case**: $O(n)$, if the array is already sorted, only one forward and one backward scan is needed.
  - **Average case**: $O(n^2)$, because it scans in both directions, average performance is similar to bubble sort.

- **Space complexity**: $O(1)$, cocktail sort is an in-place algorithm and does not need extra storage space.

#### 4. Code example of cocktail sort

```go
package main

import "fmt"

// cocktail sort
func cocktailSort(arr []int) {
    n := len(arr)
    if n <= 1 {
        return
    }

    // initialize pointers
    left, right := 0, n-1
    for left < right {
        // forward scan
        swapped := false
        for i := left; i < right; i++ {
            if arr[i] > arr[i+1] {
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = true
            }
        }
        right--

        // no swaps means the array is already sorted
        if !swapped {
            break
        }

        // backward scan
        swapped = false
        for i := right; i > left; i-- {
            if arr[i] < arr[i-1] {
                arr[i], arr[i-1] = arr[i-1], arr[i]
                swapped = true
            }
        }
        left++
    }
}

func main() {
    arr := []int{5, 1, 4, 2, 8, 6, 3, 7}
    fmt.Println("Original array:", arr)
    cocktailSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of cocktail sort

Compared with unidirectional bubble sort, cocktail sort sorts from both ends in one round, so partially sorted data takes fewer scan rounds; the cost is maintaining scans in two directions, which makes the implementation more complex than bubble sort. Its worst case is still $O(n^2)$, so it is not a good choice for large-scale data.

### Summary

Cocktail sort is bidirectional bubble sort: in one round it sinks large values left to right, then floats small values right to left. An already-sorted array is confirmed in a single forward and backward scan, with complexity $O(n)$; data that does not sort well is still $O(n^2)$, on par with bubble sort.

## References

- [Cocktail Shaker Sort · Wikipedia](https://en.wikipedia.org/wiki/Cocktail_shaker_sort)

## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CountingSort](/algo/sort/CountingSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
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
