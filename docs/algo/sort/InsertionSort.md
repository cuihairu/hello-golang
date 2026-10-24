### Insertion Sort

Insertion sort is a simple sorting algorithm whose core idea is to insert elements one by one into the already sorted portion, gradually bringing the whole list into order. It is much like how we sort a hand of playing cards: each time we take a new card and insert it into the already sorted cards, keeping the whole hand ordered.

#### 1. The basics of insertion sort

Start from the second element of the list, compare it against the already sorted portion one element at a time, and insert it at the right position. Each inserted element grows the sorted portion by one, until every element is in place.

#### 2. Algorithm steps of insertion sort

Here are the detailed steps of insertion sort:

1. **Outer loop**: start from the second element of the list.
   - The current element `key` is the one being inserted into the sorted portion.

2. **Inner loop**: walk backwards from the end of the sorted portion to find where `key` belongs.
   - Move elements greater than `key` one position back.

3. **Insert**:
   - Put `key` into the position found, keeping the sorted portion in order.

#### 3. Time and space complexity of insertion sort

- **Time complexity**:
  - **Worst case**: $O(n^2)$, when the array is fully reversed, every insertion has to walk through the whole sorted portion.
  - **Best case**: $O(n)$, when the array is already sorted, a single pass is enough and the insertion is linear time.
  - **Average case**: $O(n^2)$, sorting a randomly ordered array averages to $O(n^2)$.

- **Space complexity**:
  - **Space complexity**: $O(1)$, insertion sort is an in-place algorithm and needs no extra storage beyond the variable used for insertion.

#### 4. Code example of insertion sort

Below is insertion sort implemented in Go:

```go
package main

import "fmt"

// InsertionSort sorts a slice of integers using insertion sort
func InsertionSort(arr []int) {
    n := len(arr)
    for i := 1; i < n; i++ {
        key := arr[i]
        j := i - 1
        // move elements greater than key one position back
        for j >= 0 && arr[j] > key {
            arr[j+1] = arr[j]
            j--
        }
        // insert key into its correct position
        arr[j+1] = key
    }
}

func main() {
    arr := []int{64, 34, 25, 12, 22, 11, 90}
    fmt.Println("Original array:", arr)
    InsertionSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of insertion sort

**Pros**:
- Simple to implement and easy to understand and write.
- Works well on small datasets or nearly sorted data.
- Stable sorting algorithm (elements with equal values keep their relative order).

**Cons**:
- Time complexity is $O(n^2)$, so it is inefficient on large datasets.
- Not suited for large amounts of data or data that is far from ordered.

### Summary

Insertion sort puts each new element into the right spot in the sorted portion. It is $O(n)$ when the array is already ordered, $O(n^2)$ when it is fully reversed, and sorts in place without extra space. The implementation is simple, which is enough for small or nearly ordered data, but it falls apart once the data grows.

## References

- [Insertion sort · Wikipedia](https://en.wikipedia.org/wiki/Insertion_sort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [HeapSort](/algo/sort/HeapSort.md)
- [MergeSort](/algo/sort/MergeSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [HeapSort](/algo/sort/HeapSort.md)
- [MergeSort](/algo/sort/MergeSort.md)
