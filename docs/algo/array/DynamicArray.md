# Dynamic Array
In Go, the dynamic array is handled by the slice (`slice`). Slices are Go's most commonly used dynamic array implementation; their length can grow and shrink with the elements.

### Slice Overview

A slice (`slice`) represents a contiguous sequence of elements and is a dynamic view over an underlying array; both its length and its capacity can change at runtime.

### Basic Concepts of Slices

1. **Slice structure**:
   A slice consists of three parts:
   - **Pointer (`ptr`)**: points to the start of the underlying array.
   - **Length (`len`)**: the number of elements the slice contains.
   - **Capacity (`cap`)**: the number of elements from the start of the slice to the end of the underlying array.

   For example, a slice of length 5 may have capacity 10, meaning its underlying array can hold 10 elements.

2. **Creating a slice**:
   - **From an array**:
     ```go
     arr := [5]int{1, 2, 3, 4, 5}
     slice := arr[1:4] // create a slice cut out of the array
     fmt.Println(slice) // [2 3 4]
     ```
   - **With the `make` function**:
     ```go
     slice := make([]int, 3) // create a slice of length 3, capacity defaults to 3
     slice = make([]int, 3, 5) // create a slice of length 3 and capacity 5
     fmt.Println(slice, len(slice), cap(slice)) // [0 0 0] 3 5
     ```
   - **From an existing slice**:
     ```go
     s1 := []int{1, 2, 3}
     s2 := s1[1:3] // create a slice cut out of an existing slice
     fmt.Println(s2) // [2 3]
     ```

### Slice Operations

1. **Accessing and modifying elements**:
   - Access and modify elements in a slice by index.
   ```go
   slice := []int{10, 20, 30}
   slice[1] = 25 // modify the second element
   fmt.Println(slice[1]) // prints 25
   ```

2. **Slice growth**:
   - When appending elements to a slice, if the slice's capacity is insufficient, Go automatically grows the underlying array.
   ```go
   slice := []int{1, 2, 3}
   slice = append(slice, 4, 5) // automatic growth
   ```

3. **Slice operation functions**:
   - **`append`**:
     ```go
     slice := []int{1, 2, 3}
     slice = append(slice, 4, 5) // append elements to the slice
     ```
   - **`copy`**:
     ```go
     src := []int{1, 2, 3}
     dest := make([]int, 2)
     copy(dest, src) // copy src into dest
     ```

4. **Slicing a slice**:
   - **Creating a sub-slice**:
     ```go
     slice := []int{1, 2, 3, 4, 5}
     subSlice := slice[1:4] // from index 1 to 3 (4 excluded)
     fmt.Println(subSlice) // [2 3 4]
     ```

### Slice Performance

Index reads and writes are O(1): pointer plus index computes the address in one step. `append` is also O(1) when capacity is available; when it is not, the underlying array is reallocated at double size and the existing elements are copied — a single O(n) operation, but n consecutive `append` calls still amortize to O(1). Inserting or deleting at the front is O(n), since every element after it has to shift by one.

Slices share their underlying array, so writing through one slice may change another slice's data — and when something goes wrong, the source is often hard to trace. To isolate, use `copy` to duplicate, or use `s[i:j:j]` to cap the capacity.

### Slice Example Code

Here are a few common slice operations:

```go
package main

import (
    "fmt"
)

func main() {
    // create a slice
    slice := []int{1, 2, 3, 4, 5}
    fmt.Println("Original Slice:", slice)

    // slice the slice
    subSlice := slice[1:4]
    fmt.Println("Sub Slice:", subSlice)

    // modify the slice
    slice[2] = 10
    fmt.Println("Modified Original Slice:", slice)
    fmt.Println("Sub Slice After Modification:", subSlice)

    // append elements
    slice = append(slice, 6, 7)
    fmt.Println("Slice After Append:", slice)

    // create a slice with make
    newSlice := make([]int, 3, 5)
    fmt.Println("New Slice:", newSlice)

    // copy a slice
    src := []int{1, 2, 3}
    dest := make([]int, len(src))
    copy(dest, src)
    fmt.Println("Destination Slice After Copy:", dest)
}
```

### Summary

A slice describes a stretch of an underlying array with three fields — pointer, length, capacity — and `append` grows it at double size when capacity runs out, which may reallocate memory. Multiple slices can share the same underlying array, and a change in one place ripples into the other slices; this is the most common source of slice bugs.

## References

- [Dynamic array · Wikipedia](https://en.wikipedia.org/wiki/Dynamic_array)
- [Official Blog · Go Slices: usage and internals](https://go.dev/blog/slices-intro)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Array](/algo/array/Array.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)
- [DoubleEndedQueue](/algo/array/DoubleEndedQueue.md)
- [MultidimensionalArray](/algo/array/MultidimensionalArray.md)
- [PriorityQueue](/algo/array/PriorityQueue.md)
- [SparseArray](/algo/array/SparseArray.md)
- [glossary](/glossary.md)
