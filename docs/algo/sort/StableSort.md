### Stable sort

A stable sorting algorithm keeps the relative order of equal elements unchanged: two elements that are equal before sorting remain in the same relative order after sorting. Multi-field sorting depends on this — first sort by the secondary field, then use a stable algorithm to sort by the primary field, and the secondary field's order is preserved.

### Common stable sorting algorithms

1. **Bubble Sort**
   - **Time complexity**:
     - Worst case: $O(n^2)$
     - Average case: $O(n^2)$
     - Best case: $O(n)$ (when the array is already sorted)
   - **Space complexity**: $O(1)$
   - **Stability**: stable

2. **Insertion Sort**
   - **Time complexity**:
     - Worst case: $O(n^2)$
     - Average case: $O(n^2)$
     - Best case: $O(n)$ (when the array is already sorted)
   - **Space complexity**: $O(1)$
   - **Stability**: stable

3. **Merge Sort**
   - **Time complexity**:
     - Worst case: $O(n \log n)$
     - Average case: $O(n \log n)$
     - Best case: $O(n \log n)$
   - **Space complexity**: $O(n)$
   - **Stability**: stable

4. **Counting Sort**
   - **Time complexity**:
     - Worst case: $O(n + k)$ where $k$ is the maximum value in the range
   - **Space complexity**: $O(k)$
   - **Stability**: stable

5. **Radix Sort**
   - **Time complexity**:
     - Worst case: $O(n \cdot k)$ where $k$ is the number of digits of the radix
   - **Space complexity**: $O(n + k)$
   - **Stability**: stable

### Choosing a stable sorting algorithm

- **Applicable scenarios**:
  - When you need to sort by multiple fields, stable sorting preserves the results of earlier field sorts.
  - When the dataset is small, or when space complexity is not a concern, merge sort is worth considering.

- **Pros and cons**:
  - **Pros**: preserves the relative order of equal elements, which multi-field sorting relies on.
  - **Cons**: some stable sorting algorithms (such as merge sort) may be worse than unstable ones (such as quick sort and heap sort) in time and space complexity.

### Code examples (Go)

Here are Go implementations of several stable sorting algorithms:

#### Insertion sort

```go
package main

import "fmt"

func insertionSort(arr []int) {
	for i := 1; i < len(arr); i++ {
		key := arr[i]
		j := i - 1
		for j >= 0 && arr[j] > key {
			arr[j+1] = arr[j]
			j--
		}
		arr[j+1] = key
	}
}

func main() {
	arr := []int{12, 11, 13, 5, 6}
	insertionSort(arr)
	fmt.Println("Sorted array:", arr)
}
```

#### Merge sort

```go
package main

import "fmt"

func mergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return arr
	}

	mid := len(arr) / 2
	left := mergeSort(arr[:mid])
	right := mergeSort(arr[mid:])

	return merge(left, right)
}

func merge(left, right []int) []int {
	result := []int{}
	i, j := 0, 0
	for i < len(left) && j < len(right) {
		if left[i] <= right[j] {
			result = append(result, left[i])
			i++
		} else {
			result = append(result, right[j])
			j++
		}
	}
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

func main() {
	arr := []int{12, 11, 13, 5, 6}
	sorted := mergeSort(arr)
	fmt.Println("Sorted array:", sorted)
}
```

Small scale, simple to implement, insertion sort is enough; for large amounts of data when space is not a concern, choose merge sort.

## References

- [Sorting algorithms · Wikipedia](https://en.wikipedia.org/wiki/Sorting_algorithm)
- [sort standard library](https://pkg.go.dev/sort)


## Sibling pages

- [BubbleSort](/algo/sort/BubbleSort.md)
- [BucketSort](/algo/sort/BucketSort.md)
- [CocktailSort](/algo/sort/CocktailSort.md)
- [Sort](/algo/sort/Sort.md)
- [TimSort](/algo/sort/TimSort.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Sort](/algo/sort/Sort.md)
- [TimSort](/algo/sort/TimSort.md)
