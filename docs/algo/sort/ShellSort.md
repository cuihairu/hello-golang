### Shell Sort

Shell sort is an improvement on insertion sort, proposed by Donald Shell in 1959: split the array into groups by a gap, run insertion sort on each group, then shrink the gap step by step. Worst-case time complexity is $O(n^2)$, but in practice it is usually much faster than plain insertion sort.

#### 1. The basic idea of Shell sort

The core idea of Shell sort is:
1. **Choose a gap sequence**: pick a sequence of gaps; this sequence splits the array into several subarrays, where elements in each subarray are spaced by the gap value.
2. **Grouped insertion sort**: run insertion sort on the subarray corresponding to each gap value. As the gap shrinks step by step, the whole array gradually becomes close to sorted.
3. **Shrink the gap step by step**: shrink the gap according to the gap sequence, until the gap reaches 1, at which point one full insertion sort is performed.

#### 2. The algorithm steps of Shell sort

1. **Choose a gap sequence**: for example 1, 4, 13, 40, 121. These gap sequences usually follow some mathematical rule; common ones are the Shell gap sequence and the Hibbard gap sequence.

2. **Grouped insertion sort**: for each gap value, group elements whose indices differ by that value into a group, and run insertion sort on each group.

3. **Shrink the gap step by step**: shrink the gap according to the sequence; when it reaches 1, do one full insertion sort and you are done.

#### 3. Time and space complexity of Shell sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$; the exact complexity depends on the choice of gap sequence.
  - **Best case**: $O(n \log n)$; for some specific gap sequences, Shell sort can achieve time complexity close to $O(n \log n)$.
  - **Average case**: $O(n \log^2 n)$; the exact complexity depends on the choice of gap sequence and the distribution of the input data.

- **Space complexity**:
  - **Space complexity**: $O(1)$; Shell sort is an in-place sorting algorithm and needs no extra storage for the sorted result.

#### 4. A code example of Shell sort

```go
package main

import "fmt"

// ShellSort performs Shell sort on a slice of integers
func ShellSort(arr []int) {
    n := len(arr)
    gap := n / 2

    // progressively shrink the gap
    for gap > 0 {
        // run insertion sort on the subarray for each gap value
        for i := gap; i < n; i++ {
            temp := arr[i]
            j := i
            // insertion sort
            for j >= gap && arr[j-gap] > temp {
                arr[j] = arr[j-gap]
                j -= gap
            }
            arr[j] = temp
        }
        gap /= 2 // shrink the gap
    }
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    ShellSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of Shell sort

**Pros**:
- **Faster than insertion sort**: compared with plain insertion sort, Shell sort is faster in practice, especially noticeable on medium-sized data.
- **In-place sorting**: needs no extra storage and no complex data structures.

**Cons**:
- **Complex time complexity**: Shell sort's time complexity depends on the choice of gap sequence, with a worst case of $O(n^2)$.
- **Unstable sort**: Shell sort is not a stable sorting algorithm; elements with equal values may change relative order.

### Summary

Shell sort finishes in place; the code is three nested loops — an outer one that shrinks the gap and an inner one that does insertion sort by step. Worst case $O(n^2)$, average about $O(n \log^2 n)$, both depending on the choice of gap sequence; it is unstable, so elements with equal values may change relative order.

## References

- [Shell sort · Wikipedia](https://en.wikipedia.org/wiki/Shellsort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [SelectionSort](/algo/sort/SelectionSort.md)
- [Sort](/algo/sort/Sort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [SelectionSort](/algo/sort/SelectionSort.md)
- [Sort](/algo/sort/Sort.md)
