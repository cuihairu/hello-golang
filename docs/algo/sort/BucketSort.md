### Bucket Sort

Bucket sort is a non-comparison sorting algorithm, suitable for sorting uniformly distributed data. It distributes the data into a group of buckets, sorts each bucket separately (usually with another sorting algorithm such as insertion sort), and finally merges the elements from the buckets to produce the final sorted result. Under specific conditions, bucket sort's time complexity can reach $O(n + k)$, where $n$ is the number of elements to sort and $k$ is the number of buckets.

#### 1. The basics of bucket sort

The core idea of bucket sort is:
1. **Determine the number of buckets and their ranges**: split the data range into several buckets.
2. **Distribute data into buckets**: based on each value, place the data into the corresponding bucket.
3. **Sort each bucket**: sort the data inside each bucket.
4. **Merge the data from the buckets**: merge the buckets in order into a single sorted output array.

#### 2. Algorithm steps of bucket sort

First, based on the maximum, minimum, and data range, determine the number of buckets and the interval each bucket covers; then traverse the data, placing each element into its corresponding bucket. Within a bucket, use a stable algorithm like insertion sort to sort it, and finally merge the data from the buckets into the result array in bucket order.

#### 3. Time and space complexity of bucket sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$, when the sorting algorithm inside a bucket (such as insertion sort) is inefficient, the time complexity is $O(n^2)$.
  - **Best case**: $O(n + k)$, when the data is uniformly distributed and bucket sorting is efficient, the time complexity is $O(n + k)$.
  - **Average case**: $O(n + k)$, the time complexity is usually $O(n + k)$.

- **Space complexity**: $O(n + k)$, extra space is needed to store the buckets and the sorted result.

#### 4. Code example of bucket sort

The following is a bucket sort algorithm implemented in Go:

```go
package main

import (
    "fmt"
    "sort"
)

// BucketSort sorts an int slice using bucket sort
func BucketSort(arr []int) {
    if len(arr) == 0 {
        return
    }

    // 1. find the minimum and maximum values
    minVal, maxVal := arr[0], arr[0]
    for _, v := range arr {
        if v < minVal {
            minVal = v
        }
        if v > maxVal {
            maxVal = v
        }
    }

    // 2. determine the number of buckets
    bucketCount := maxVal - minVal + 1
    buckets := make([][]int, bucketCount)

    // 3. distribute data into buckets
    for _, v := range arr {
        index := v - minVal
        buckets[index] = append(buckets[index], v)
    }

    // 4. sort each bucket and merge
    resultIndex := 0
    for _, bucket := range buckets {
        if len(bucket) > 0 {
            sort.Ints(bucket) // use Go's built-in sort function to sort the bucket's data
            for _, v := range bucket {
                arr[resultIndex] = v
                resultIndex++
            }
        }
    }
}

func main() {
    arr := []int{29, 25, 3, 49, 9, 37, 21, 43}
    fmt.Println("Original array:", arr)
    BucketSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of bucket sort

**Pros**:
- When the data is uniformly distributed, the time complexity is close to linear at $O(n + k)$.
- It can handle data with a large value range.

**Cons**:
- Performs poorly when the data is unevenly distributed; the time complexity can degrade to $O(n^2)$.
- Requires $O(n + k)$ of extra space to store the buckets and the sorted result.
- The number of buckets and their ranges must be chosen reasonably; a poor split will slow down sorting.

### Summary

Bucket sort does not compare elements; it partitions by value range into buckets to complete the sort. When the data is uniformly distributed it is $O(n + k)$, and when the distribution is uneven it degrades to $O(n^2)$, while also paying $O(n + k)$ of extra space. It suits data with a known value range and a roughly uniform distribution.

## References

- [Bucket Sort · Wikipedia](https://en.wikipedia.org/wiki/Bucket_sort)

## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [CountingSort](/algo/sort/CountingSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BubbleSort](/algo/sort/BubbleSort.md)
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
