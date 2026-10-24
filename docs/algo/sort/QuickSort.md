### Quick Sort

Quick sort was introduced by Tony Hoare in 1960. The idea is to pick a pivot element, split the array in two around it, and sort each half on its own — divide and conquer. Its average time complexity is $O(n \log n)$, and it is the most commonly used general-purpose sort.

#### 1. The basics of quick sort

The basic idea of quick sort is:
1. **Pick a pivot**: choose one element from the array to be sorted as the pivot.
2. **Partition**: rearrange the array so that every element smaller than the pivot is to its left and every element larger than the pivot is to its right.
3. **Sort recursively**: recursively quick sort the subarrays on either side of the pivot.

#### 2. Algorithm steps of quick sort

In code, one round of partitioning goes like this:

1. **Pick a pivot**: the code takes the last element of the array (`arr[high]`); taking the first, or a random one, is also common.
2. **Partition**: index `i` marks out the "less than or equal to the pivot" region; while scanning, elements that match get swapped into that region, and at the end the pivot is swapped to the end of the region, fixing its position.
3. **Sort recursively**: recurse on the subarrays on either side of the pivot, and stop when a subarray has length 1 or less.

#### 3. Time and space complexity of quick sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$, when the array is already sorted or fully reversed, the partition can end up very unbalanced and drive the time complexity up to $O(n^2)$.
  - **Best case**: $O(n \log n)$, when every partition splits the array evenly, the time complexity is $O(n \log n)$.
  - **Average case**: $O(n \log n)$, sorting a randomly ordered array averages to $O(n \log n)$.

- **Space complexity**: $O(\log n)$, from the recursion stack; the sort runs on the original array and takes no extra storage.

#### 4. Code example of quick sort

Here is the Go implementation:

```go
package main

import "fmt"

// Partition performs the partition step, splitting the array into two parts
func Partition(arr []int, low, high int) int {
    pivot := arr[high] // pick the last element as the pivot
    i := low - 1      // end index of the region of elements smaller than the pivot

    for j := low; j < high; j++ {
        if arr[j] <= pivot {
            i++
            arr[i], arr[j] = arr[j], arr[i]
        }
    }

    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
}

// QuickSort quick sorts a slice of integers
func QuickSort(arr []int, low, high int) {
    if low < high {
        pi := Partition(arr, low, high)
        QuickSort(arr, low, pi-1)
        QuickSort(arr, pi+1, high)
    }
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    QuickSort(arr, 0, len(arr)-1)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of quick sort

**Pros**:
- Average $O(n \log n)$, with elements swapped inside the original array and no extra storage.

**Cons**:
- When the array is already sorted or fully reversed, each partition degenerates and the time complexity falls back to $O(n^2)$.
- Not stable; elements with equal values may swap places.

### Summary

Each round of quick sort does one thing: move the pivot to where it belongs. Average $O(n \log n)$, in place, not stable, and it degrades to $O(n^2)$ on arrays that are already sorted or fully reversed.

## References

- [Quick sort · Wikipedia](https://en.wikipedia.org/wiki/Quicksort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [MergeSort](/algo/sort/MergeSort.md)
- [RadixSort](/algo/sort/RadixSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [MergeSort](/algo/sort/MergeSort.md)
- [RadixSort](/algo/sort/RadixSort.md)
