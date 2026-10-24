### Radix Sort

Radix sort is a non-comparison sort. It groups the data by digit (or character), then uses a stable sorting algorithm (such as counting sort) to sort one position at a time from the lowest to the highest; once the top position is done, the whole array is ordered. The time complexity is $O(n \cdot k)$, where $n$ is the number of elements to sort and $k$ is the largest number of digits or characters. It fits cases with lots of data but a small radix (numbers, for example).

#### 1. The basics of radix sort

The basic idea of radix sort is:
1. **Determine the number of positions**: find the longest digit count or character count in the data.
2. **Sort from the lowest to the highest position**: sort each position in order from low to high. A stable sorting algorithm (such as counting sort) can be used.

#### 2. Algorithm steps of radix sort

1. **Determine the number of positions**: find the longest digit count or character count in the data to be sorted.
2. **Sort by position**: starting at the least significant digit (LSD, Least Significant Digit), sort each position in turn until the most significant digit (MSD, Most Significant Digit).
3. **Use a stable sorting algorithm**: apply a stable sort such as counting sort to each position, so that elements sharing the same digit keep their original relative order.

#### 3. Time and space complexity of radix sort

- **Time complexity**: best, worst, and average are all $O(n \cdot k)$, and it does not change with the distribution of the input data.
- **Space complexity**: $O(n + k)$, extra space is needed for the sorted result and the count array.

#### 4. Code example of radix sort

```go
package main

import "fmt"

// getMax returns the largest value in the array
func getMax(arr []int) int {
    max := arr[0]
    for _, v := range arr {
        if v > max {
            max = v
        }
    }
    return max
}

// countingSort sorts the array by a given digit position using counting sort
func countingSort(arr []int, exp int) {
    n := len(arr)
    output := make([]int, n) // output array
    count := make([]int, 10) // count array

    // count how often each digit occurs
    for i := 0; i < n; i++ {
        index := (arr[i] / exp) % 10
        count[index]++
    }

    // accumulate the count array
    for i := 1; i < 10; i++ {
        count[i] += count[i-1]
    }

    // sort by digit position
    for i := n - 1; i >= 0; i-- {
        index := (arr[i] / exp) % 10
        output[count[index]-1] = arr[i]
        count[index]--
    }

    // copy the sorted result back into the original array
    for i := 0; i < n; i++ {
        arr[i] = output[i]
    }
}

// RadixSort radix sorts a slice of integers
func RadixSort(arr []int) {
    max := getMax(arr)

    // sort from the lowest digit to the highest
    for exp := 1; max/exp > 0; exp *= 10 {
        countingSort(arr, exp)
    }
}

func main() {
    arr := []int{170, 45, 75, 90, 802, 24, 2, 66}
    fmt.Println("Original array:", arr)
    RadixSort(arr)
    fmt.Println("Sorted array:", arr)
}
```

#### 5. Pros and cons of radix sort

Radix sort never compares elements against each other: a number with $k$ positions gets $k$ passes, and every pass uses a stable sort, so elements with equal values keep their original relative order; it shines especially when the range of integers is bounded. The cost has two parts: space — the count array plus the output array take $O(n + k)$ — and data type — it only works on integers or characters and cannot sort things like floating-point numbers. The implementation also has to handle the per-digit logic that a simple sort does not.

### Summary

Radix sort groups by digit and runs counting sort position by position: $n$ elements with $k$ positions means $O(n \cdot k)$, no matter how the input is distributed. Stability and a fixed number of passes make it a good fit for data like integers and strings; what it costs is $O(n + k)$ of extra space, and the limitation that floating-point numbers cannot be sorted this way.

## References

- [Radix sort · Wikipedia](https://en.wikipedia.org/wiki/Radix_sort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [QuickSort](/algo/sort/QuickSort.md)
- [SelectionSort](/algo/sort/SelectionSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [QuickSort](/algo/sort/QuickSort.md)
- [SelectionSort](/algo/sort/SelectionSort.md)
