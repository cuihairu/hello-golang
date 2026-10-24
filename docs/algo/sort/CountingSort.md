### Counting Sort

Counting sort is a non-comparison sorting algorithm, suitable for sorting elements with a limited integer range. Its basic idea is to sort by counting the number of occurrences of each element in the array. Counting sort has a time complexity of $O(n + k)$, where $n$ is the number of elements to sort and $k$ is the range of element values. It performs no comparisons between elements, so when $k$ is not much larger than $n$, this complexity beats the $O(n \log n)$ of comparison sorts.

#### 1. The basics of counting sort

The basic steps of counting sort are as follows:
1. **Determine the range**: find the maximum and minimum values in the array to sort, establishing the range of element values.
2. **Count occurrences**: create a count array to record how often each element appears.
3. **Accumulate counts**: accumulate the elements of the count array to determine each element's position in the sorted array.
4. **Build the sorted result**: use the accumulated count array to reconstruct the sorted array.

#### 2. Algorithm steps of counting sort

1. **Determine the range**:
   - Find the maximum and minimum values of the array to sort.
   - Compute the range of element values $k = \text{max} - \text{min} + 1$.

2. **Count occurrences**:
   - Create a count array `count` of size $k$, initialized to 0.
   - Traverse the array to sort, and increment the corresponding position in the count array for each element.

3. **Accumulate counts**:
   - Accumulate the count array to compute each element's position in the sorted array.
   - The accumulated count array can be used to determine each element's final position in the sorted array.

4. **Build the sorted result**:
   - Traverse the array to sort, placing each element into the sorted array, with the position determined by the accumulated count array.

#### 3. Time and space complexity of counting sort

- **Time complexity**:
  - **Worst case**: $O(n + k)$, where $n$ is the number of elements to sort and $k$ is the range of element values.
  - **Best case**: $O(n + k)$, in all cases counting sort has a time complexity of $O(n + k)$.
  - **Average case**: $O(n + k)$, the time complexity is not affected by the distribution of the input data.

- **Space complexity**:
  - **Space complexity**: $O(n + k)$, extra space is needed to store the count array and the sorted result array.

#### 4. Code example of counting sort

The following is a counting sort algorithm implemented in Go:

```go
package main

import "fmt"

// CountingSort sorts an int slice using counting sort
func CountingSort(arr []int) {
    if len(arr) == 0 {
        return
    }

    // find the maximum and minimum values
    maxVal, minVal := arr[0], arr[0]
    for _, v := range arr {
        if v > maxVal {
            maxVal = v
        }
        if v < minVal {
            minVal = v
        }
    }

    // create the count array
    rangeSize := maxVal - minVal + 1
    count := make([]int, rangeSize)

    // count occurrences
    for _, v := range arr {
        count[v-minVal]++
    }

    // compute the accumulated counts
    for i := 1; i < len(count); i++ {
        count[i] += count[i-1]
    }

    // build the sorted result
    output := make([]int, len(arr))
    for i := len(arr) - 1; i >= 0; i-- {
        output[count[arr[i]-minVal]-1] = arr[i]
        count[arr[i]-minVal]--
    }

    // copy the sorted result back into the original array
    copy(arr, output)
}

func main() {
    arr := []int{4, 2, 2, 8, 3, 3, 1}
    fmt.Println("Original array:", arr)
    CountingSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of counting sort

**Pros**:
- **Linear time complexity**: when the range of element values $k$ is not much larger than the number of elements $n$, counting sort achieves linear time complexity $O(n + k)$.
- **Stable sort**: counting sort is a stable algorithm; elements with equal values keep their original relative order.
- **Simple implementation**: counting sort is relatively simple to implement and requires no complex comparison operations.

**Cons**:
- **High space complexity**: for a very large value range, counting sort needs a lot of extra space and may not be suitable for a wide range of values.
- **Not suitable for floats or negatives**: counting sort is mainly for integers; handling floats or negative numbers requires extra steps.
- **Limited by the value range**: when the value range $k$ is large, the space complexity of counting sort grows significantly, hurting performance.

### Summary

Counting sort does not compare elements; it sorts by counting occurrences, with a time complexity of $O(n + k)$ and it is stable. The premise is integers with a limited value range: once $k$ grows, the $O(n + k)$ space cost becomes a hard limitation.

## References

- [Counting Sort · Wikipedia](https://en.wikipedia.org/wiki/Counting_sort)

## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [HeapSort](/algo/sort/HeapSort.md)
