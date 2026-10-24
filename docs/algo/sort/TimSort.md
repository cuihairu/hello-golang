### Timsort

Timsort was designed by Tim Peters in 2002 for Python's sorting library: it first uses insertion sort to cut the data into ordered small blocks, then uses merging to combine those blocks into a fully ordered whole. Both Python and Java's `Arrays.sort()` use it.

#### 1. The basic idea of Timsort

Timsort's approach:
1. **Run splitting**: divide the data to be sorted into several ordered blocks (called "runs").
2. **Use insertion sort**: run insertion sort on the data inside each small block (run), ensuring every block is ordered.
3. **Merge sort**: use merge sort to combine these ordered blocks into one fully ordered result.

#### 2. The algorithm steps of Timsort

Walk through it with the code, in three steps:

1. **Run splitting**:
   - Split the data to be sorted into blocks, with the block size fixed by a parameter, usually between 32 and 64.

2. **Use insertion sort**:
   - Run insertion sort block by block. The blocks are small, which is exactly the sweet spot for insertion sort, and it picks up on any order already present in the data.

3. **Merge sort**:
   - Use merge sort to combine the ordered blocks into one fully ordered result. The merging process of merge sort is carried out efficiently through a priority queue (such as a min-heap).

#### 3. Time and space complexity of Timsort

- **Time complexity**: worst, best and average cases are all $O(n \log n)$, the same as merge sort.

- **Space complexity**: $O(n)$, because merging needs extra temporary arrays.

#### 4. A code example of Timsort

Here is a simplified Go implementation, with a block size of 32:

```go
package main

import (
    "fmt"
    "math"
)

// insertion sort
func insertionSort(arr []int, left, right int) {
    for i := left + 1; i <= right; i++ {
        key := arr[i]
        j := i - 1
        for j >= left && arr[j] > key {
            arr[j+1] = arr[j]
            j--
        }
        arr[j+1] = key
    }
}

// merge function
func merge(arr []int, l, m, r int) {
    n1 := m - l + 1
    n2 := r - m

    // create temporary arrays
    L := make([]int, n1)
    R := make([]int, n2)

    // copy data into the temporary arrays
    copy(L, arr[l:l+n1])
    copy(R, arr[m+1:m+1+n2])

    // merge the temporary arrays
    i, j, k := 0, 0, l
    for i < n1 && j < n2 {
        if L[i] <= R[j] {
            arr[k] = L[i]
            i++
        } else {
            arr[k] = R[j]
            j++
        }
        k++
    }

    // copy the remaining elements
    for i < n1 {
        arr[k] = L[i]
        i++
        k++
    }

    for j < n2 {
        arr[k] = R[j]
        j++
        k++
    }
}

// Timsort
func timSort(arr []int) {
    n := len(arr)
    run := 32 // size of the small blocks
    for i := 0; i < n; i += run {
        end := int(math.Min(float64(i+run-1), float64(n-1)))
        insertionSort(arr, i, end)
    }

    size := run
    for size < n {
        for left := 0; left < n; left += 2 * size {
            mid := int(math.Min(float64(left+size-1), float64(n-1)))
            right := int(math.Min(float64(left+2*size-1), float64(n-1)))
            if mid < right {
                merge(arr, left, mid, right)
            }
        }
        size *= 2
    }
}

func main() {
    arr := []int{5, 21, 7, 23, 19, 17}
    fmt.Println("Original array:", arr)
    timSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of Timsort

**Pros**:
- Stable sort, so equal elements keep their relative order after sorting.
- Insertion sort exploits locally ordered data blocks; the better the order within a block, the fewer comparisons.

**Cons**:
- The implementation has to handle three pieces of logic — splitting into blocks, insertion sort per block, and pairwise merging — so it is longer than a simple sorting algorithm.
- Merging needs $O(n)$ extra space.

### Summary

Timsort puts insertion sort and merging together: insertion sort within blocks, merging between blocks, $O(n \log n)$ in all three time cases, with $O(n)$ extra space. This is the algorithm behind Python and Java's `Arrays.sort()`.

## References

- [Timsort · Wikipedia](https://en.wikipedia.org/wiki/Timsort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [StableSort](/algo/sort/StableSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [StableSort](/algo/sort/StableSort.md)
