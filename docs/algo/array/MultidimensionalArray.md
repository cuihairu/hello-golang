# Multidimensional Array
A multidimensional array is an array of arrays: every level is an array, a 2D array holds several 1D arrays, a 3D array holds several 2D arrays, and so on, with an index given for each level when reading a value.

### Basic Concepts of a Multidimensional Array

1. **Definition and initialization**:
   A multidimensional array can be defined by nesting arrays. For example, a 2D array can be viewed as an array containing several 1D arrays, and a 3D array as an array containing several 2D arrays, and so on.

   ```go
   var arr [2][3]int // 2D array, containing 2 1D arrays, each with 3 integers
   fmt.Println(arr) // [[0 0 0] [0 0 0]]
   ```

   You can also give the initialization list directly:

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }
   fmt.Println(arr) // [[1 2 3] [4 5 6]]
   ```

2. **Accessing and modifying elements**:
   When accessing or modifying elements of a multidimensional array, an index for every dimension must be specified.

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }
   
   fmt.Println(arr[0][1]) // prints 2
   arr[1][2] = 7
   fmt.Println(arr[1][2]) // prints 7
   ```

3. **Multidimensional arrays of dynamic length**:
   Go array lengths are fixed and cannot be changed at runtime. If you need to add or remove elements dynamically, use a slice (`slice`), which can be resized at runtime.

   ```go
   // definition and initialization of a 2D slice
   rows := 2
   cols := 3
   matrix := make([][]int, rows)
   for i := range matrix {
       matrix[i] = make([]int, cols)
   }

   matrix[0][0] = 1
   matrix[1][2] = 7
   ```

4. **Iterating a multidimensional array**:
   Use nested `for` loops to iterate over the elements of a multidimensional array.

   ```go
   arr := [2][3]int{
       {1, 2, 3},
       {4, 5, 6},
   }

   for i := range arr {
       for j := range arr[i] {
           fmt.Printf("%d ", arr[i][j])
       }
       fmt.Println()
   }
   ```

### Example Code

```go
package main

import (
    "fmt"
)

func main() {
    // define and initialize a 2D array
    arr := [2][3]int{
        {1, 2, 3},
        {4, 5, 6},
    }
    
    // access and modify elements
    fmt.Println("Element at [0][1]:", arr[0][1])
    arr[1][2] = 7
    fmt.Println("Modified element at [1][2]:", arr[1][2])
    
    // iterate the 2D array
    fmt.Println("Elements in 2D array:")
    for i := range arr {
        for j := range arr[i] {
            fmt.Printf("%d ", arr[i][j])
        }
        fmt.Println()
    }
    
    // create and initialize a 2D slice
    rows := 2
    cols := 3
    matrix := make([][]int, rows)
    for i := range matrix {
        matrix[i] = make([]int, cols)
    }
    
    matrix[0][0] = 1
    matrix[1][2] = 7
    
    // iterate the 2D slice
    fmt.Println("Elements in 2D slice:")
    for i := range matrix {
        for j := range matrix[i] {
            fmt.Printf("%d ", matrix[i][j])
        }
        fmt.Println()
    }
}
```

### Summary

### Complexity

A single indexed read or write is O(1): a multidimensional index collapses into one address offset. Iterating an $m \times n$ array visits every element, O(mn). Array lengths are fixed, with no insertion or deletion; if rows and columns need to change, switch to a 2D slice — rebuilding an entire row is O(n).

### Summary

A multidimensional array is an array of arrays with fixed lengths, suited to data whose rows and columns are known. If rows and columns need to vary, use a 2D slice, where each row is allocated separately. Definition, indexing, assignment, and iteration with nested `for` loops all look the same in both forms.

## References

- [Array (data structure) · Wikipedia](https://en.wikipedia.org/wiki/Array_data_structure)


## Sibling pages

- [DynamicArray](/algo/array/DynamicArray.md)
- [Array](/algo/array/Array.md)
- [CircularBuffer](/algo/array/CircularBuffer.md)
- [PriorityQueue](/algo/array/PriorityQueue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [PriorityQueue](/algo/array/PriorityQueue.md)
