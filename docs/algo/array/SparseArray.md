# Sparse Array

A Sparse Array is a compressed storage scheme used to hold a 2D array in which many elements are zero (or the same default value). It only records "the coordinates and values of the non-zero elements," trading $m \times n$ of storage for $k+1$ rows of triples.

### Algorithm Overview

1. **Counting**: scan the original array and count the number of non-zero elements `sum`.
2. **Building the sparse array**: the sparse array is a `(sum+1) × 3` table, where row 0 records the number of rows, number of columns, and number of non-zero elements of the original array; each subsequent row records one `row, col, value` triple for a non-zero element.
3. **Restoring**: read row 0 to recover the original array's dimensions, then walk through the triples and write each non-zero element back to its coordinate.

### Algorithm Steps

1. **Compressing**:
   - Traverse the original 2D array and collect all non-zero elements into a list of triples.

2. **Restoring**:
   - Create a new array using the row and column counts from row 0 and zero out everything.
   - Walk through the triples and execute `arr[row][col] = value`.

### Code Example (Go Implementation)

```go
package main

import "fmt"

// toSparse compresses a 2D array into a sparse array
func toSparse(arr [][]int) [][]int {
	sum := 0
	for _, row := range arr {
		for _, v := range row {
			if v != 0 {
				sum++
			}
		}
	}
	sparse := make([][]int, sum+1)
	sparse[0] = []int{len(arr), len(arr[0]), sum}
	idx := 1
	for i, row := range arr {
		for j, v := range row {
			if v != 0 {
				sparse[idx] = []int{i, j, v}
				idx++
			}
		}
	}
	return sparse
}

// fromSparse restores a 2D array from a sparse array
func fromSparse(sparse [][]int) [][]int {
	rows, cols := sparse[0][0], sparse[0][1]
	arr := make([][]int, rows)
	for i := range arr {
		arr[i] = make([]int, cols)
	}
	for _, item := range sparse[1:] {
		arr[item[0]][item[1]] = item[2]
	}
	return arr
}

func main() {
	arr := [][]int{
		{0, 0, 3, 0, 0},
		{0, 5, 0, 0, 0},
		{0, 0, 0, 0, 0},
		{7, 0, 0, 2, 0},
	}
	sparse := toSparse(arr)
	fmt.Println("Sparse array:")
	for _, row := range sparse {
		fmt.Println(row)
	}

	restored := fromSparse(sparse)
	fmt.Println("Restored array:")
	for _, row := range restored {
		fmt.Println(row)
	}
}
```

Runtime output:

```text
Sparse array:
[4 5 4]
[0 2 3]
[1 1 5]
[3 0 7]
[3 3 2]
Restored array:
[0 0 3 0 0]
[0 5 0 0 0]
[0 0 0 0 0]
[7 0 0 2 0]
```

### Complexity Analysis

Let the original array be $m \times n$ with $k$ non-zero elements:

- **Compressing**: time $O(mn)$, space $O(k)$.
- **Restoring**: time $O(mn + k)$, space $O(mn)$.
- When $k \ll mn$, the storage of the sparse array is far smaller than that of the original array.

### Application Scenarios

- Storing data with large blank areas, such as game boards and maps.
- Storing and computing sparse matrices (such as an adjacency matrix of a graph).

### Summary

A sparse array records a small amount of useful data as "coordinate + value" triples, replacing $O(mn)$ of storage with $O(k)$ of space. Game-board archives and sparse-matrix storage are its typical scenarios.

## References

- [Sparse matrix · Wikipedia](https://en.wikipedia.org/wiki/Sparse_matrix)


## Sibling pages

- [DynamicArray](/algo/array/DynamicArray.md)
- [Array](/algo/array/Array.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)
- [PriorityQueue](/algo/array/PriorityQueue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [PriorityQueue](/algo/array/PriorityQueue.md)
