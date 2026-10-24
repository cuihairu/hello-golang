# Array


> Perspective: this page discusses arrays from the data-structure angle — their contiguous storage and operations. For Go's array type, value semantics, and the slice counterpart, see [Go Array Notes](/type/Array.md).
An Array is the most basic linear data structure. It stores a group of same-typed elements in a contiguous block of memory, and an element's address can be computed directly from its index, giving $O(1)$ random access.

### Characteristics of Arrays

1. **Contiguous storage**: elements sit in a contiguous block of memory, which is friendly to the CPU cache.
2. **Random access**: a known index goes straight to the element, time complexity $O(1)$.
3. **Fixed length**: in Go the length `N` of `[N]T` is part of the type and cannot change after declaration.
4. **Value type**: Go arrays are value types; assignment and passing arguments copy the entire array.

### Basic Operations

1. **Declaration and initialization**:
   - `var a [3]int`: length 3, elements at their zero values.
   - `a := [3]int{1, 2, 3}`: declare and initialize.
   - `b := [...]int{1, 2, 3}`: length inferred from the number of initial values.

2. **Access and modification**: `a[i]`. An out-of-bounds index errors at compile time (constant index) or at runtime.

3. **Iteration**: `for i := 0; i < len(a); i++` or `for i, v := range a`.

4. **Multidimensional arrays**: `[2][3]int` denotes a 2-row, 3-column 2D array.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// sum computes the sum of array elements (the array is copied by value into the call)
func sum(a [5]int) int {
	total := 0
	for _, v := range a {
		total += v
	}
	return total
}

func main() {
	// declare and initialize
	a := [5]int{3, 1, 4, 1, 5}
	// length inferred from the number of initial values
	b := [...]string{"Go", "C", "Python"}

	// modify an element
	a[0] = 10

	// iterate
	for i, v := range a {
		fmt.Printf("a[%d] = %d\n", i, v)
	}

	// 2D array
	var matrix [2][3]int
	for i := range matrix {
		for j := range matrix[i] {
			matrix[i][j] = i*3 + j
		}
	}
	fmt.Println("matrix =", matrix)

	fmt.Println("len(a) =", len(a), "sum =", sum(a))
	fmt.Println("b =", b)
}
```

Runtime output:

```text
a[0] = 10
a[1] = 1
a[2] = 4
a[3] = 1
a[4] = 5
matrix = [[0 1 2] [3 4 5]]
len(a) = 5 sum = 21
b = [Go C Python]
```

### Arrays and Slices

- An array has a fixed length and is a value type; a slice has a variable length and is a view over an underlying array.
- Slicing an array with `a[1:3]` gives a slice that shares memory with the original array, so modifying the slice affects the array.
- Slices are used more often in day-to-day development, but a slice cannot do without the array providing that "underlying contiguous memory."

### Complexity Analysis

- **Access**: $O(1)$, addressing directly by index.
- **Lookup**: $O(n)$; an unordered array requires a linear scan.
- **Insertion/deletion**: a fixed-length array has no dynamic insert or delete; making room in the middle, or pulling elements together, requires moving subsequent elements and costs $O(n)$.

### Summary

An array trades contiguous memory for the fastest random-access speed, and it underlies many other structures: slices, dynamic arrays, hash buckets, and more. In Go, arrays are value types and the length is part of the type, so array semantics are usually used through slices.

## References

- [Array (data structure) · Wikipedia](https://en.wikipedia.org/wiki/Array_data_structure)

## Sibling pages

- [DynamicArray](/algo/array/DynamicArray.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)
- [DoubleEndedQueue](/algo/array/DoubleEndedQueue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [CircularBuffer](/algo/array/CircularBuffer.md)
- [DoubleEndedQueue](/algo/array/DoubleEndedQueue.md)
- [MultidimensionalArray](/algo/array/MultidimensionalArray.md)
- [PriorityQueue](/algo/array/PriorityQueue.md)
- [SparseArray](/algo/array/SparseArray.md)
