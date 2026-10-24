### Merge Sort

Merge sort is a divide-and-conquer sorting algorithm. It breaks a big problem into many small ones, solves those recursively, and then merges the results into the final ordered sequence. Its time complexity is $O(n \log n)$, and it is a stable sort.

#### 1. The basics of merge sort

The process of merge sort splits into two main steps:

1. **Divide**:
   - Split the array to be sorted in half, and recursively sort the two halves, until each subarray holds a single element.

2. **Merge**:
   - Merge the sorted subarrays into one ordered array. The merge step combines two sorted subarrays into a single new sorted subarray.

#### 2. Algorithm steps of merge sort

1. **Divide**:
   - If the array has more than one element, split it into two roughly equal parts.
   - Recursively merge sort the two parts.

2. **Merge**:
   - Create a new array to hold the merged result.
   - Walk the two sorted subarrays with two pointers, inserting the smaller element into the new array each time.
   - When one subarray is exhausted, copy the remaining elements of the other straight into the new array.

3. **Return the result**:
   - Return the merged, ordered array.

#### 3. Time and space complexity of merge sort

- **Time complexity**:
  - **Worst case**: $O(n \log n)$, the divide and merge phases cost $O(\log n)$ and $O(n)$, whose product gives $O(n \log n)$.
  - **Best case**: $O(n \log n)$, no matter what the input looks like, the time complexity stays $O(n \log n)$.
  - **Average case**: $O(n \log n)$, sorting a randomly ordered array averages to $O(n \log n)$.

- **Space complexity**: $O(n)$, extra storage is needed to hold the merged result.

#### 4. Code example of merge sort

Below is merge sort implemented in Go:

```go
package main

import "fmt"

// Merge combines two sorted slices into one ordered slice
func Merge(left, right []int) []int {
    result := []int{}
    i, j := 0, 0

    // merge the two sorted slices
    for i < len(left) && j < len(right) {
        if left[i] < right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }

    // append the remaining elements to the result slice
    for i < len(left) {
        result = append(result, left[i])
        i++
    }
    for j < len(right) {
        result = append(result, right[j])
        j++
    }

    return result
}

// MergeSort merge sorts a slice of integers
func MergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }

    mid := len(arr) / 2
    left := MergeSort(arr[:mid])
    right := MergeSort(arr[mid:])
    return Merge(left, right)
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    sortedArray := MergeSort(arr)
    fmt.Println("Sorted array:", sortedArray)
}
```

#### 5. Pros and cons of merge sort

**Pros**:
- **Stable sort**: merge sort is a stable algorithm, so elements with equal values keep their relative order.
- **Time complexity**: $O(n \log n)$, which performs well on large datasets.
- **Broad applicability**: it can be used to sort linked lists and other data structures.

**Cons**:
- **Space complexity**: extra storage is needed to hold the merged result, so space complexity is $O(n)$.
- **Not in place**: because of the extra space, merge sort does not fit environments with tight memory.

### Summary

Merge sort splits the array into smaller subarrays and sorts them recursively, then merges them back into one ordered array. The price is $O(n)$ of extra space; what you get in return is a stable $O(n \log n)$ that does not depend on the input, which suits large datasets and any case where the relative order of elements must be kept.

## References

- [Merge sort · Wikipedia](https://en.wikipedia.org/wiki/Merge_sort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [InsertionSort](/algo/sort/InsertionSort.md)
- [QuickSort](/algo/sort/QuickSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [InsertionSort](/algo/sort/InsertionSort.md)
- [QuickSort](/algo/sort/QuickSort.md)
